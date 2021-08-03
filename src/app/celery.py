from celery import Celery

celery = Celery("app.app")
celery.config_from_object('app.celeryconfig')
celery.conf.task_track_started = True
