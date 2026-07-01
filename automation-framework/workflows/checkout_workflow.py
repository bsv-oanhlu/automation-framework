from playwright.sync_api import Page

from data.loader import load_json
from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.product_detail_page import ProductDetailPage
from workflows.auth_workflow import login_as_standard_user

checkout_data = load_json("checkout.json")


def prepare_cart_with_item(page: Page, product_name: str) -> CartPage:
    inventory_page = login_as_standard_user(page)
    inventory_page.add_product_to_cart(product_name)
    inventory_page.go_to_cart()
    return CartPage(page)


def prepare_checkout_info_page(page: Page, product_name: str) -> CheckoutInfoPage:
    cart_page = prepare_cart_with_item(page, product_name)
    cart_page.proceed_to_checkout()
    return CheckoutInfoPage(page)


def prepare_checkout_overview_page(page: Page, product_name: str) -> CheckoutOverviewPage:
    checkout_info_page = prepare_checkout_info_page(page, product_name)
    info = checkout_data["validInfo"]
    checkout_info_page.fill_checkout_info(info["firstName"], info["lastName"], info["postalCode"])
    return checkout_info_page.submit_and_continue()


def prepare_checkout_complete_page(page: Page, product_name: str) -> CheckoutCompletePage:
    overview_page = prepare_checkout_overview_page(page, product_name)
    return overview_page.finish_order()


def prepare_product_detail_page(page: Page, product_name: str) -> ProductDetailPage:
    inventory_page = login_as_standard_user(page)
    inventory_page.open_product_detail(product_name)
    return ProductDetailPage(page)
