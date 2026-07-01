from playwright.sync_api import Locator, Page

from locators.product_detail_locators import ProductDetailLocators
from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.product_name: Locator = page.locator(ProductDetailLocators.PRODUCT_NAME)
        self.product_description: Locator = page.locator(ProductDetailLocators.PRODUCT_DESCRIPTION)
        self.product_price: Locator = page.locator(ProductDetailLocators.PRODUCT_PRICE)
        self.add_to_cart_button: Locator = page.locator(ProductDetailLocators.ADD_TO_CART_BUTTON)
        self.back_to_products_link: Locator = page.locator(ProductDetailLocators.BACK_TO_PRODUCTS)
        self.product_image: Locator = page.locator(ProductDetailLocators.PRODUCT_IMAGE)

    def add_to_cart(self) -> None:
        self.add_to_cart_button.click()

    def remove_from_cart(self) -> None:
        self.add_to_cart_button.click()

    def back_to_products(self):
        from pages.inventory_page import InventoryPage

        self.back_to_products_link.click()
        self.page.wait_for_url("**/inventory.html")
        return InventoryPage(self.page)
