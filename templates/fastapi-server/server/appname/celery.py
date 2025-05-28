import logging
from celery import Celery
from .config import settings
from .database import get_db

celery_app = Celery(
    'worker', 
    broker=settings.BROKER_URL,
    backend=settings.BROKER_URL
)

celery_app.conf.update(
    task_routes={
        'tasks.*': {'queue': 'default'}
    },
)

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

setup_logging()