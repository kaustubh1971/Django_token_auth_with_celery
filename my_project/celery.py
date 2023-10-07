from __future__ import absolute_import, unicode_literals
import os

from celery.schedules import crontab
from celery import Celery
from django.conf import settings
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')

app = Celery('my_project')
app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'Task_one_schedule' : {  # whatever the name you want
        'task': 'user_app.tasks.test_func', # name of task with path
        'schedule': crontab(hour=3, minute=18), # crontab() runs the tasks every minute
    },
    'Task_two_schedule' : {  # whatever the name you want
        'task': 'user_app.tasks.test_date', # name of task with path
        'schedule': 3000, # 30 runs this task every 3000 seconds
        'args' : [datetime.now()] # arguments for the task
    },
}


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
