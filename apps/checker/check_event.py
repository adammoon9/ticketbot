from playwright.sync_api import (
    Browser,
    Locator,
    Page,
    TimeoutError,
    expect,
)
import re

PRICE_RE = re.compile(r"(||)\s?\d")


def check_for_quickpicks(page: Page, timeout_ms: int = 2500):
    quickpicks_list = page.locator(selector="#quickpicks-list")
    if not quickpicks_list.count() or not quickpicks_list:
        return False
    try:
        quickpicks_list.wait_for(state="visible", timeout=timeout_ms)
        try:
            expect(quickpicks_list).not_to_have_text("Loading...", timeout=timeout_ms)
        except TimeoutError:
            pass
    except Exception:
        return False

    qp_text = quickpicks_list.inner_text(timeout=timeout_ms)

    if PRICE_RE.search(qp_text):
        return True


def parse_view_tickets(page: Page, timeout_ms: int = 5000):
    possible_ticks = page.get_by_test_id("reserveView")
    possible_ticks.wait_for(state="visible", timeout=timeout_ms)

    is_expired = possible_ticks.locator(':text("Time Expired")')
    if is_expired.count() and is_expired.first.is_visible():
        return False

    no_tickets_left = possible_ticks.locator(
        ':text("There aren\'t enough tickets to complete your request")'
    )
    if no_tickets_left.count() and no_tickets_left.first.is_visible():
        return False

    ticket_info = possible_ticks.get_by_test_id("ticketTypeInfo").first
    if ticket_info.count() and ticket_info.first.is_visible():
        return True

    return False


def check_for_find_tickets(page: Page, timeout_ms: int = 12000):
    ticket_amt_selector = page.get_by_role("spinbutton").first
    find_tickets_button = page.get_by_role(
        "button", name=re.compile(r"(find|buy) tickets", re.IGNORECASE)
    )
    ticket_amt_selector.wait_for(state="visible", timeout=timeout_ms)
    if not ticket_amt_selector.count() or not ticket_amt_selector:
        return False

    try:
        _ = set_spinbutton_qty(ticket_amt_selector, target=1, max_steps=10)
        try:
            expect(find_tickets_button).to_be_enabled(timeout=timeout_ms)
            find_tickets_button.click()
            result = parse_view_tickets(page=page)

            return result
        except TimeoutError:
            return False
    except Exception:
        return False


def set_spinbutton_qty(
    locator: Locator, target: int = 1, max_steps: int = 20, timeout_ms: int = 5000
):
    locator.wait_for(state="visible", timeout=timeout_ms)

    def convert_aria_to_int(attr: str, default: int = 0):
        val = locator.get_attribute(attr)
        try:
            return int(val) if val is not None else default
        except Exception:
            return default

    curr_val = convert_aria_to_int("aria-valuenow", 0)

    locator.focus()
    steps = 0
    while (curr_val == 0 or curr_val < target) and steps < max_steps:
        locator.press("ArrowUp")
        curr_val = convert_aria_to_int("aria-valuenow", curr_val)
        steps += 1

    return curr_val


def fetch_tm_event(event_url: str, browser: Browser, timeout_ms: int = 12000):
    context = browser.new_context(locale="en-IE", timezone_id="Europe/Dublin")
    page = context.new_page()

    page_response = page.goto(
        url=event_url, wait_until="domcontentloaded", timeout=timeout_ms
    )
    page_status = page_response.status if page_response else 404

    if page_status == 404:
        return False

    head = page.content()[:1000].lower()
    if '"response": "identify"' in head or "captcha" in head or "virtual queue" in head:
        browser.close()
        return

    for sel in ['button:has-text("Accept Cookies")', 'button:has-text("I agree")']:
        try:
            page.click(sel, timeout=timeout_ms)
            break
        except Exception:
            pass

    if check_for_quickpicks(page=page):
        return True

    if check_for_find_tickets(page=page):
        return True

    context.close()
    browser.close()

    return False
