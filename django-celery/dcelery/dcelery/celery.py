from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcelery.settings')
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")

# @app.task # register the task with celery
# def add_numbers():
#     return

app.autodiscover_tasks() # looks for tasks.py file inside all installed apps