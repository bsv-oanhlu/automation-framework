from playwright.sync_api import Locator, Page

from components.header import HeaderComponent
from components.sidebar import SidebarComponent


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.header = HeaderComponent(page)
        self.sidebar = SidebarComponent(page)

    @property
    def shopping_cart_badge(self) -> Locator:
        return self.header.cart_badge

    @property
    def shopping_cart_link(self) -> Locator:
        return self.header.cart_link

    @property
    def menu_button(self) -> Locator:
        return self.sidebar.menu_button

    def open_menu(self) -> None:
        self.sidebar.open()

    def logout(self) -> None:
        self.sidebar.logout()

    def reset_app_state(self) -> None:
        self.sidebar.reset_app_state()

    def go_to_cart(self) -> None:
        self.header.go_to_cart()

    def get_cart_badge_count(self) -> str | None:
        return self.header.get_cart_badge_count()
