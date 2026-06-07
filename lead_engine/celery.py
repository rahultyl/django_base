import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lead_engine.settings.local")

app = Celery("lead_engine")
task = app.task
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
