web: gunicorn main:app
worker: celery --app main.celery worker
beat: celery --app main.celery beat