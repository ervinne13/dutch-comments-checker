import logging
from celery import Celery

logging.basicConfig(level=logging.INFO)

# TODO: Hardcode for now
celery_app = Celery(
    'dcc_tasks',
    broker='redis://dcc_redis:6379/0',
    backend='redis://dcc_redis:6379/0'
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
