from playwright.sync_api import Locator, Page

from locators.cart_locators import CartLocators
from locators.common_locators import CommonLocators
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page_title: Locator = page.locator(CommonLocators.PAGE_TITLE)
        self.cart_items: Locator = page.locator(CartLocators.CART_ITEM)
        self.continue_shopping_button: Locator = page.locator(CartLocators.CONTINUE_SHOPPING)
        self.checkout_button: Locator = page.locator(CartLocators.CHECKOUT)

    def goto(self) -> None:
        self.page.goto("/cart.html")
        self.page.wait_for_url("**/cart.html")

    def get_cart_item_by_name(self, name: str) -> Locator:
        return self.page.locator(
            CartLocators.CART_ITEM,
            has=self.page.locator(CommonLocators.INVENTORY_ITEM_NAME, has_text=name),
        )

    def remove_item(self, product_name: str) -> None:
        self.get_cart_item_by_name(product_name).locator("button", has_text="Remove").click()

    def continue_shopping(self):
        from pages.inventory_page import InventoryPage

        self.continue_shopping_button.click()
        self.page.wait_for_url("**/inventory.html")
        return InventoryPage(self.page)

    def proceed_to_checkout(self):
        from pages.checkout_info_page import CheckoutInfoPage

        self.checkout_button.click()
        self.page.wait_for_url("**/checkout-step-one.html")
        return CheckoutInfoPage(self.page)

    def get_cart_item_names(self) -> list[str]:
        names = self.page.locator(
            f"{CartLocators.CART_ITEM} {CommonLocators.INVENTORY_ITEM_NAME}"
        ).all_text_contents()
        return [n.strip() for n in names]

    def get_cart_item_price(self, product_name: str) -> str:
        item = self.get_cart_item_by_name(product_name)
        return item.locator(CommonLocators.INVENTORY_ITEM_PRICE).text_content() or ""

    def get_item_quantity(self, product_name: str) -> str:
        item = self.get_cart_item_by_name(product_name)
        return item.locator(CartLocators.CART_QUANTITY).text_content() or ""

    def get_item_remove_button(self, product_name: str) -> Locator:
        return self.get_cart_item_by_name(product_name).locator("button")

    def get_item_price_element(self, product_name: str) -> Locator:
        return self.get_cart_item_by_name(product_name).locator(
            CommonLocators.INVENTORY_ITEM_PRICE
        )
