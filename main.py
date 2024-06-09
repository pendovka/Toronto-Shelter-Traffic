from flask import Flask, jsonify
from flask_cors import CORS
from celery import Celery
from celery.schedules import crontab
from output import get_predictions
from redis import Redis 
import os


password = os.environ['REDIS_PASSWORD']

app = Flask(__name__)
CORS(app, send_wildcard=True)

celery = Celery(
    __name__,
    broker=f"redis://default:{password}@redis-11824.c325.us-east-1-4.ec2.redns.redis-cloud.com:11824",
    backend=f"redis://default:{password}@redis-11824.c325.us-east-1-4.ec2.redns.redis-cloud.com:11824"
)

celery.conf.update(
    task_track_started=True,
    beat_schedule={
        'schedule_print_predictions': {  # Name of the periodic task
            'task': 'main.print_predictions',  
            'schedule': crontab(hour='*/12'),  # Schedule task to run every 12 hours
        },
    }
)

r = Redis(
  host='redis-11824.c325.us-east-1-4.ec2.redns.redis-cloud.com', 
  port=11824,
  password=password)

@app.route('/')
def index():
    return 'hi'

@celery.task     
def print_predictions():
    predictions = get_predictions()
    return predictions 


@app.route('/get_predictions')  
def route_get_predictions():

    current_task_id = r.get("current_task_id")
    
    if not current_task_id:
        task = print_predictions.apply_async(None, expires=60*60*7)
        r.set("current_task_id", task.id, ex = 6*60*60)

    current_task = print_predictions.AsyncResult(r.get('current_task_id'))

    if current_task.status == 'SUCCESS':
        r.set('last_completed_task_id', current_task.id)

    elif current_task.status == 'FAILURE':
        r.delete("current_task_id")
        return jsonify({'result': None}), 500
        
    last_completed_task_id = r.get("last_completed_task_id")

    if last_completed_task_id:
        task = print_predictions.AsyncResult(last_completed_task_id)

        if task.status == 'SUCCESS':
            return jsonify({
                'result': task.result,
                'completed_on': task.date_done  
            }), 200
            
    return jsonify({'result': None, 'status': 'PENDING'}), 202



