from playwright.sync_api import Locator, Page

from locators.common_locators import CommonLocators


class HeaderComponent:
    def __init__(self, page: Page):
        self.page = page
        self.cart_badge: Locator = page.locator(CommonLocators.SHOPPING_CART_BADGE)
        self.cart_link: Locator = page.locator(CommonLocators.SHOPPING_CART_LINK)

    def go_to_cart(self) -> None:
        self.cart_link.click()
        self.page.wait_for_url("**/cart.html")

    def get_cart_badge_count(self) -> str | None:
        if self.cart_badge.is_visible():
            return self.cart_badge.text_content()
        return None
