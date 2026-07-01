from playwright.sync_api import Locator, Page

from locators.checkout_locators import CheckoutCompleteLocators
from locators.common_locators import CommonLocators
from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page_title: Locator = page.locator(CommonLocators.PAGE_TITLE)
        self.complete_header: Locator = page.locator(CheckoutCompleteLocators.COMPLETE_HEADER)
        self.complete_text: Locator = page.locator(CheckoutCompleteLocators.COMPLETE_TEXT)
        self.pony_express_text: Locator = page.locator(CheckoutCompleteLocators.PONY_EXPRESS)
        self.back_home_button: Locator = page.locator(CheckoutCompleteLocators.BACK_HOME)

    def back_home(self):
        from pages.inventory_page import InventoryPage

        self.back_home_button.click()
        self.page.wait_for_url("**/inventory.html")
        return InventoryPage(self.page)
