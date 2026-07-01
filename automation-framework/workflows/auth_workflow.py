from playwright.sync_api import Page

from data.loader import load_json
from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_detail_page import ProductDetailPage

users = load_json("users.json")


def login_as_standard_user(page: Page) -> InventoryPage:
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(users["validUser"]["username"], users["validUser"]["password"])
    page.wait_for_url("**/inventory.html")
    return InventoryPage(page)


def login_with_credentials(page: Page, username: str, password: str) -> None:
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(username, password)
