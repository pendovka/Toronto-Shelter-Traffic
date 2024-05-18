from flask import Flask, jsonify
from flask_cors import CORS
from celery import Celery
from model import get_predictions
from redis import Redis 
import os

password = os.environ['REDIS_PASSWORD']

app = Flask(__name__)
CORS(app, send_wildcard=True)

celery = Celery(
    __name__,
    broker=f"redis://default:{password}@redis-15429.c11.us-east-1-2.ec2.redns.redis-cloud.com:15429",
    backend=f"redis://default:{password}@redis-15429.c11.us-east-1-2.ec2.redns.redis-cloud.com:15429"
)
celery.conf.update(task_track_started=True)

r = Redis(
  host='redis-15429.c11.us-east-1-2.ec2.redns.redis-cloud.com',
  port=15429,
  password=password)

@app.route('/')
def index():
    return 'hi'

@celery.task
def print_predictions():
    return get_predictions()


@app.route('/get_predictions')
def route_get_predictions():

    current_task_id = r.get("current_task_id")
    if not current_task_id:
        task = print_predictions.delay()
        r.set("current_task_id", task.id)
        r.expire("current_task_id", 600)
        return jsonify({
            'status': 'Accepted'
            }), 202
    else:
        task = print_predictions.AsyncResult(current_task_id)
        if task.state == 'PENDING' or task.state == 'STARTED':
            response = {
                'state': task.state,
                'status': 'Pending...'
            }
            status = 202

        elif task.state == 'FAILURE':
            response = {
                'state': task.state,
                'result': task.result
            }
            r.delete("current_task_id")
            status = 500

        elif task.state == 'SUCCESS':
            response = {
                'state': task.state,
                'result': task.result
            }
            status = 200
        

        return jsonify(response), status
    