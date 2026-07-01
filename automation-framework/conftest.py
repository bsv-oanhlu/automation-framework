import sys
from pathlib import Path

import pytest
from playwright.sync_api import expect

from config.playwright import (
    BASE_URL,
    DEFAULT_TIMEOUT,
    EXPECT_TIMEOUT,
    NAVIGATION_TIMEOUT,
)

sys.path.insert(0, str(Path(__file__).parent))


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": BASE_URL,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": True,
    }


@pytest.fixture(autouse=True)
def configure_playwright_timeouts(page):
    page.set_default_timeout(DEFAULT_TIMEOUT)
    page.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
    expect.set_options(timeout=EXPECT_TIMEOUT)
