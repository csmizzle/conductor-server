import os
from celery import Celery
import logfire
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from celery.signals import worker_process_init


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conductor_server.settings")

# set up logging and logfire
logfire.configure()


@worker_process_init.connect(weak=False)
def init_celery_tracing(*args, **kwargs):
    CeleryInstrumentor().instrument()


app = Celery("proj")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.update(
    WORKER_MAX_TASKS_PER_CHILD=1,
)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
