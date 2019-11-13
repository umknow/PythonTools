# -*- coding=utf-8 -*-
# datetime: 2019/4/10 13:27

"""
    celery连接管理器包
"""

from quotations.conf import config
from celery import Celery
from celery import platforms
platforms.C_FORCE_ROOT = True


class CeleryManager:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(CeleryManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, settings):
        self.tasks = Celery("tasks", broker=settings['CELERY_BROKER_URL'])
        self.tasks.conf.update(settings)

    def get_task(self):
        return self.tasks


def get_task():
    settings=config('celery').get()
    celery_manager=CeleryManager(settings)
    return celery_manager.get_task()


tasks = get_task()
# print(tasks)
