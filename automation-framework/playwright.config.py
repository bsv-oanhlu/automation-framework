"""
Playwright configuration — tương đương playwright.config.ts.

Cấu hình chi tiết nằm trong config/playwright.py.
File này là entry point theo yêu cầu deliverable.
"""

from config.playwright import (  # noqa: F401
    BASE_URL,
    BROWSERS,
    DEFAULT_TIMEOUT,
    EXPECT_TIMEOUT,
    NAVIGATION_TIMEOUT,
    PARALLEL_WORKERS,
    PYTEST_ADDOPTS,
)

__all__ = [
    "BASE_URL",
    "DEFAULT_TIMEOUT",
    "EXPECT_TIMEOUT",
    "NAVIGATION_TIMEOUT",
    "BROWSERS",
    "PARALLEL_WORKERS",
    "PYTEST_ADDOPTS",
]
