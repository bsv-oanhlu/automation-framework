from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from data.loader import load_json
from workflows import prepare_checkout_complete_page

products = load_json("products.json")


class TestCheckoutComplete:
    def test_tc01_display_checkout_complete_page(self, page: Page):
        complete_page = prepare_checkout_complete_page(page, products["backpack"]["name"])

        expect(complete_page.page_title).to_have_text("Checkout: Complete!")
        expect(complete_page.complete_header).to_have_text("Thank you for your order!")
        expect(complete_page.complete_text).to_be_visible()
        expect(complete_page.complete_text).to_contain_text(
            "Your order has been dispatched, and will arrive just as fast as the pony can get there!"
        )
        expect(complete_page.pony_express_text).to_be_visible()
        expect(complete_page.back_home_button).to_be_visible()

    def test_tc02_back_home_after_complete(self, page: Page):
        complete_page = prepare_checkout_complete_page(page, products["backpack"]["name"])
        inventory_page = complete_page.back_home()

        expect(inventory_page.page_title).to_have_text("Products")
        expect(inventory_page.shopping_cart_badge).not_to_be_visible()

    def test_tc03_empty_cart_after_order_complete(self, page: Page):
        complete_page = prepare_checkout_complete_page(page, products["backpack"]["name"])
        complete_page.go_to_cart()

        cart_page = CartPage(page)
        expect(cart_page.page_title).to_have_text("Your Cart")
        expect(cart_page.cart_items).to_have_count(0)
