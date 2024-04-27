from flask import Flask, jsonify
from celery import Celery
from model import get_predictions


app = Flask(__name__)

celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)

@app.route('/')
def index():
    return 'hi'


@celery.task
def print_predictions():
    return get_predictions()

@app.route('/check_task/<task_id>')
def check_task(task_id):
    task = print_predictions.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'result': task.result
        }
    else:
        response = {
            'state': task.state,
        }
    return jsonify(response)

@app.route('/start_task')
def start_task():
    task = print_predictions.delay()  
    return jsonify({'task_id': task.id}), 202  # 202 Accepted status code
