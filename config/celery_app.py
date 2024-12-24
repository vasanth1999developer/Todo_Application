import os
from celery.schedules import crontab
from celery import Celery
from django.utils.module_loading import import_string

from config import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("apps")



# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Register class based tasks are not auto registered by default.
# Ref: https://github.com/celery/celery/issues/5992#issuecomment-781857785
for _import_string in []:
    app.register_task(import_string(_import_string)())

broker_connection_retry_on_startup = True
def is_beat_debug():
    """
    Returns if the celery beat is running on debug mode. Debug mode is used for
    development purposes on the local environment.
    """

    return settings.APP_SWITCHES["CELERY_BEAT_DEBUG_MODE"]


app.conf.beat_schedule={  
    "sent-email-at-9am-every-day": {
        "task": "todo.tasks.send_task_reminder_emails_morning",
        "schedule": crontab(hour=9, minute=0)
    },
    "sent-email-at-4pm-every-day":{
        "task": "todo.tasks.send_task_reminder_emails_evening",
        "schedule": crontab(hour=17, minute=23)
    }
}
