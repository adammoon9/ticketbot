from .celery_app import app
from .playwright_singleton import get_browser, shutdown_browser
from celery.signals import worker_process_init, worker_process_shutdown


@worker_process_init.connect
def __init_browser():
    get_browser()


@worker_process_shutdown.connect
def _shutdown_browser():
    shutdown_browser()
