from playwright.sync_api import Locator, Page, expect

from locators.common_locators import CommonLocators
from locators.inventory_locators import InventoryLocators
from pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page_title: Locator = page.locator(CommonLocators.PAGE_TITLE)
        self.inventory_items: Locator = page.locator(InventoryLocators.INVENTORY_ITEM)
        self.sort_dropdown: Locator = page.locator(InventoryLocators.SORT_DROPDOWN)

    def goto(self) -> None:
        self.page.goto("/inventory.html")
        self.page.wait_for_url("**/inventory.html")

    def get_product_by_name(self, name: str) -> Locator:
        return self.page.locator(
            InventoryLocators.INVENTORY_ITEM,
            has=self.page.locator(CommonLocators.INVENTORY_ITEM_NAME, has_text=name),
        )

    def add_product_to_cart(self, product_name: str) -> None:
        product = self.get_product_by_name(product_name)
        product.locator("button", has_text="Add to cart").click()

    def remove_product_from_cart(self, product_name: str) -> None:
        product = self.get_product_by_name(product_name)
        product.locator("button", has_text="Remove").click()

    def open_product_detail(self, product_name: str) -> None:
        self.get_product_by_name(product_name).locator(
            CommonLocators.INVENTORY_ITEM_NAME
        ).click()
        self.page.wait_for_url("**/inventory-item.html**")

    def sort_by(self, option: str) -> None:
        self.sort_dropdown.select_option(option)

    def get_product_names(self) -> list[str]:
        names = self.page.locator(CommonLocators.INVENTORY_ITEM_NAME).all_text_contents()
        return [n.strip() for n in names]

    def get_product_prices(self) -> list[float]:
        prices = self.page.locator(CommonLocators.INVENTORY_ITEM_PRICE).all_text_contents()
        return [float(p.replace("$", "")) for p in prices]

    def get_add_to_cart_button(self, product_name: str) -> Locator:
        return self.get_product_by_name(product_name).locator("button")

    def verify_product_list_layout(self) -> None:
        for item in self.inventory_items.all():
            expect(item.locator(InventoryLocators.ITEM_IMG)).to_be_visible()
            expect(item.locator(CommonLocators.INVENTORY_ITEM_NAME)).to_be_visible()
            expect(item.locator(InventoryLocators.ITEM_DESC)).to_be_visible()
            expect(item.locator(CommonLocators.INVENTORY_ITEM_PRICE)).to_be_visible()
            expect(item.locator("button")).to_be_visible()

    def open_product_detail_page(self, product_name: str):
        from pages.product_detail_page import ProductDetailPage

        self.open_product_detail(product_name)
        return ProductDetailPage(self.page)
