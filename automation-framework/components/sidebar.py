from playwright.sync_api import Page

from locators.common_locators import CommonLocators


class SidebarComponent:
    def __init__(self, page: Page):
        self.page = page
        self.menu_button = page.locator(CommonLocators.MENU_BUTTON)

    def open(self) -> None:
        self.menu_button.click()

    def logout(self) -> None:
        self.open()
        self.page.locator(CommonLocators.LOGOUT_LINK).click()
        self.page.wait_for_url("/")

    def reset_app_state(self) -> None:
        self.open()
        self.page.locator(CommonLocators.RESET_LINK).click()
        self.page.reload()
        self.page.wait_for_url("**/inventory.html")
