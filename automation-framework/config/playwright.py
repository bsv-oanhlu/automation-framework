"""Playwright runtime configuration."""

from config.settings import Settings

BASE_URL = Settings.BASE_URL
DEFAULT_TIMEOUT = Settings.DEFAULT_TIMEOUT
EXPECT_TIMEOUT = Settings.EXPECT_TIMEOUT
NAVIGATION_TIMEOUT = Settings.NAVIGATION_TIMEOUT

BROWSERS = ["chromium", "firefox", "webkit"]
PARALLEL_WORKERS = "auto"

PYTEST_ADDOPTS = [
    f"-n {PARALLEL_WORKERS}",
    "--browser chromium",
    "--browser firefox",
    "--browser webkit",
    "--tracing retain-on-failure",
    "--screenshot only-on-failure",
]
