from playwright.sync_api import Locator, Page

from config.settings import Settings
from locators.checkout_locators import CheckoutInfoLocators
from locators.common_locators import CommonLocators
from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page_title: Locator = page.locator(CommonLocators.PAGE_TITLE)
        self.first_name_input: Locator = page.locator(CheckoutInfoLocators.FIRST_NAME)
        self.last_name_input: Locator = page.locator(CheckoutInfoLocators.LAST_NAME)
        self.postal_code_input: Locator = page.locator(CheckoutInfoLocators.POSTAL_CODE)
        self.continue_button: Locator = page.locator(CheckoutInfoLocators.CONTINUE)
        self.cancel_button: Locator = page.locator(CheckoutInfoLocators.CANCEL)
        self.error_message: Locator = page.locator(CommonLocators.ERROR_MESSAGE)

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def submit(self) -> None:
        self.continue_button.click()

    def submit_and_continue(self):
        from pages.checkout_overview_page import CheckoutOverviewPage

        self.continue_button.click()
        self.page.wait_for_url("**/checkout-step-two.html")
        return CheckoutOverviewPage(self.page)

    def cancel(self):
        from pages.cart_page import CartPage

        with self.page.expect_navigation(
            url="**/cart.html", timeout=Settings.NAVIGATION_TIMEOUT
        ):
            self.cancel_button.click()
        return CartPage(self.page)
