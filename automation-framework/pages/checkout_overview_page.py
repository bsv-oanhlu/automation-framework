from playwright.sync_api import Locator, Page

from locators.cart_locators import CartLocators
from locators.checkout_locators import CheckoutOverviewLocators
from locators.common_locators import CommonLocators
from pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page_title: Locator = page.locator(CommonLocators.PAGE_TITLE)
        self.cart_items: Locator = page.locator(CartLocators.CART_ITEM)
        self.item_total: Locator = page.locator(CheckoutOverviewLocators.ITEM_TOTAL)
        self.tax: Locator = page.locator(CheckoutOverviewLocators.TAX)
        self.total: Locator = page.locator(CheckoutOverviewLocators.TOTAL)
        self.payment_info: Locator = page.locator(CheckoutOverviewLocators.PAYMENT_INFO)
        self.shipping_info: Locator = page.locator(CheckoutOverviewLocators.SHIPPING_INFO)
        self.finish_button: Locator = page.locator(CheckoutOverviewLocators.FINISH)
        self.cancel_button: Locator = page.locator(CheckoutOverviewLocators.CANCEL)

    def finish_order(self):
        from pages.checkout_complete_page import CheckoutCompletePage

        self.finish_button.click()
        self.page.wait_for_url("**/checkout-complete.html")
        return CheckoutCompletePage(self.page)

    def cancel(self):
        from pages.inventory_page import InventoryPage

        self.cancel_button.click()
        self.page.wait_for_url("**/inventory.html")
        return InventoryPage(self.page)

    def get_item_total_value(self) -> float:
        text = self.item_total.text_content() or ""
        return float(text.replace("Item total: $", ""))

    def get_tax_value(self) -> float:
        text = self.tax.text_content() or ""
        return float(text.replace("Tax: $", ""))

    def get_total_value(self) -> float:
        text = self.total.text_content() or ""
        return float(text.replace("Total: $", ""))

    def get_cart_item_names(self) -> list[str]:
        names = self.page.locator(
            f"{CartLocators.CART_ITEM} {CommonLocators.INVENTORY_ITEM_NAME}"
        ).all_text_contents()
        return [n.strip() for n in names]
