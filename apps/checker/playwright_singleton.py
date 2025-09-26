from playwright.sync_api import Browser, Playwright, sync_playwright

_p: Playwright | None = None
_browser: Browser | None = None


def get_browser() -> Browser:
    global _p, _browser

    if _browser:
        return _browser

    _p = sync_playwright().start()
    _browser = _p.chromium.launch(headless=True)
    return _browser


def shutdown_browser() -> None:
    global _p, _browser
    try:
        if _browser:
            _browser.close()
    finally:
        _browser = None
        if _p:
            _p.stop()
