from time import sleep
import os
from celery import Celery

# Initialize celery
celery_app = Celery(main=__name__, include=[
    "workflows.upload.minio",
    "workflows.validate.html",
    "workflows.validate.file"
])
celery_app.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "amqp://rabbitmq:5672")
celery_app.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "db+postgresql://user:password@postgresql:5432/deployflow")

celery_app.conf.events = {
    'task-sent': True,
    'task-received': True,
    'task-started': True,
    'task-succeeded': True,
    'task-failed': True,
    'task-revoked': True,
}

celery_app.conf.worker_send_task_events = True
celery_app.conf.task_send_sent_event = True
celery_app.conf.task_track_started = True
celery_app.conf.result_extended = True
celery_app.conf.enable_utc = True

# https://docs.celeryq.dev/en/latest/userguide/configuration.html#worker
celery_app.conf.update(
    task_acks_late              = True,
    task_reject_on_worker_lost  = True,
    prefetch_multiplier         = 1,
    worker_pool_restarts        = os.environ.get("CELERY_WORKER_POOL_RESTARTS", True),
    result_expires              = None,
    task_time_limit             = os.environ.get("CELERY_TASK_TIME_LIMIT", 3600),
    worker_max_tasks_per_child  = os.environ.get("CELERY_WORKER_MAX_TASKS_PER_CHILD", 300),
    task_serializer             = 'json',
    result_serializer           = 'json',
    accept_content              = ['json'],
)

