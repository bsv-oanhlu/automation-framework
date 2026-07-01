from playwright.sync_api import Locator, Page, expect

from locators.common_locators import CommonLocators
from locators.login_locators import LoginLocators
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input: Locator = page.locator(LoginLocators.USERNAME)
        self.password_input: Locator = page.locator(LoginLocators.PASSWORD)
        self.login_button: Locator = page.locator(LoginLocators.LOGIN_BUTTON)
        self.error_message: Locator = page.locator(CommonLocators.ERROR_MESSAGE)
        self.logo: Locator = page.locator(LoginLocators.LOGO)
        self.login_credentials: Locator = page.locator(LoginLocators.LOGIN_CREDENTIALS)
        self.login_password_hint: Locator = page.locator(LoginLocators.LOGIN_PASSWORD_HINT)

    def goto(self) -> None:
        self.page.goto("/")
        self.page.wait_for_url("/")

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def wait_for_inventory_page(self, timeout: int | None = None):
        from pages.inventory_page import InventoryPage

        if timeout:
            self.page.wait_for_url("**/inventory.html", timeout=timeout)
        else:
            self.page.wait_for_url("**/inventory.html")
        return InventoryPage(self.page)
