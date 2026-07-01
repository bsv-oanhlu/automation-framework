from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from data.loader import load_json
from workflows import checkout_data, login_as_standard_user, prepare_checkout_overview_page

products = load_json("products.json")


class TestCheckoutOverview:
    def test_tc01_display_checkout_overview_page(self, page: Page):
        overview_page = prepare_checkout_overview_page(page, products["backpack"]["name"])

        expect(overview_page.page_title).to_have_text("Checkout: Overview")
        expect(overview_page.payment_info).to_have_text("SauceCard #31337")
        expect(overview_page.shipping_info).to_contain_text("Pony Express")
        expect(overview_page.cart_items).to_have_count(1)
        expect(overview_page.item_total).to_be_visible()
        expect(overview_page.tax).to_be_visible()
        expect(overview_page.total).to_be_visible()
        expect(overview_page.finish_button).to_be_visible()
        expect(overview_page.cancel_button).to_be_visible()

    def test_tc02_verify_payment_total(self, page: Page):
        overview_page = prepare_checkout_overview_page(page, products["backpack"]["name"])

        item_total = overview_page.get_item_total_value()
        tax = overview_page.get_tax_value()
        total = overview_page.get_total_value()

        assert item_total == products["backpack"]["price"]
        assert tax > 0
        assert abs(total - (item_total + tax)) < 0.01
        assert abs(total - 32.39) < 0.1

    def test_tc03_finish_order(self, page: Page):
        overview_page = prepare_checkout_overview_page(page, products["backpack"]["name"])
        complete_page = overview_page.finish_order()

        expect(complete_page.complete_header).to_have_text("Thank you for your order!")

    def test_tc04_cancel_from_overview(self, page: Page):
        overview_page = prepare_checkout_overview_page(page, products["backpack"]["name"])
        inventory_page = overview_page.cancel()

        expect(inventory_page.page_title).to_have_text("Products")
        expect(inventory_page.shopping_cart_badge).to_have_text("1")

    def test_tc05_display_two_products_on_overview(self, page: Page):
        inventory_page = login_as_standard_user(page)
        inventory_page.add_product_to_cart(products["backpack"]["name"])
        inventory_page.add_product_to_cart(products["bikeLight"]["name"])
        inventory_page.go_to_cart()

        cart_page = CartPage(page)
        checkout_info_page = cart_page.proceed_to_checkout()
        info = checkout_data["validInfo"]
        checkout_info_page.fill_checkout_info(
            info["firstName"], info["lastName"], info["postalCode"]
        )
        overview_page = checkout_info_page.submit_and_continue()

        item_names = overview_page.get_cart_item_names()
        assert products["backpack"]["name"] in item_names
        assert products["bikeLight"]["name"] in item_names

        item_total = overview_page.get_item_total_value()
        expected_total = products["backpack"]["price"] + products["bikeLight"]["price"]
        assert abs(item_total - expected_total) < 0.01
