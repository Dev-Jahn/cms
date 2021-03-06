from celery import Celery

from . import celeryconfig
from util.logger import logger

celery_app = Celery('cam_worker')
celery_app.config_from_object(celeryconfig)


class TaskManager:
    def __init__(self):
        pass

    def list_tasks(self):
        pass
