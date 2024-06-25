from celery import Celery
import requests
import os

# from testapp.models import QueueRequest, QueueResponse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tt.settings')

app = Celery('tt')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
