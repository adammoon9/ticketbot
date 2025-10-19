import os
from ..api.db import SessionLocal
from ..api.models.event import Event
from ..api.models.subscription import Subscription
from .check_event import fetch_tm_event
from contextlib import contextmanager
from playwright.sync_api import Playwright, Browser, sync_playwright
from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown
from datetime import datetime, timedelta, timezone

BROKER_URL = os.environ.get("CELERY_BROKER_URL", default="redis://redis:6379/0")
RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", default="redis://redis:6379/0")

_browser: Browser | None = None
_p: Playwright | None = None

celery = Celery(__name__, broker=BROKER_URL, backend=RESULT_BACKEND)


@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_browser() -> Browser:
    global _browser, _p
    if _browser:
        return _browser

    _p = sync_playwright().start()
    _browser = _p.chromium.launch(headless=True)
    return _browser


def close_browser() -> None:
    global _browser, _p
    try:
        if _browser:
            _browser.close()
    finally:
        _browser = None
        if _p:
            _p.stop()


@worker_process_init.connect
def _init_browser(**kwargs):
    init_browser()


@worker_process_shutdown.connect
def _shutdown_browser(**kwargs):
    close_browser()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(
        60.0, pool_subscriptions, name="Pool subscriptions every minute"
    )


@celery.task(bind=True, name="check_event", autoretry_for=(Exception,), max_retries=3)
def check_event(self, event_id: int):
    with session_scope() as db:
        event_obj = db.get(Event, event_id)
        if not event_obj:
            return {
                "status": "Failed",
                "reason": f"Could not find event obj with id: {event_id}",
            }

        url = event_obj.url
        browser = init_browser()
        result = fetch_tm_event(browser=browser, event_url=url)

        return {
            "status": "Success" if result else "Failed",
            "reason": "Found tickets" if result else "No tickets found",
        }


@celery.task(name="pool_subscriptions")
def pool_subscriptions() -> None:
    with session_scope() as db:
        active_subs = db.query(Subscription).filter_by(active=True).all()
        if not active_subs:
            return

        for sub in active_subs:
            e_id = sub.event_id
            event_obj = db.query(Event).filter_by(id=e_id).one_or_none()
            if (
                not event_obj
                or datetime.now(tz=timezone.utc) <= event_obj.next_checked_at
            ):
                continue

            _result = check_event.delay(e_id)
            event_obj.next_checked_at += timedelta(minutes=20)
            try:
                db.commit()
                db.refresh(sub)
                db.refresh(event_obj)
            except Exception:
                db.rollback()
