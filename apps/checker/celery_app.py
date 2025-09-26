import os
from celery import Celery

BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
BACKEND_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = Celery("checker", broker=BROKER_URL, backend=BACKEND_URL)
app.conf.update(
    task_acks_late=True,
    worker_prefetch_multiplier=1,  # avoid job hoarding
    task_time_limit=60,
    task_soft_time_limit=45,
)
