from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from data.loader import load_json
from workflows import login_as_standard_user, prepare_cart_with_item

products = load_json("products.json")


class TestCart:
    def test_tc01_display_cart_with_one_product(self, page: Page):
        cart_page = prepare_cart_with_item(page, products["backpack"]["name"])

        expect(cart_page.page_title).to_have_text("Your Cart")
        expect(cart_page.continue_shopping_button).to_be_visible()
        expect(cart_page.checkout_button).to_be_visible()
        expect(cart_page.get_cart_item_by_name(products["backpack"]["name"])).to_be_visible()
        assert cart_page.get_item_quantity(products["backpack"]["name"]) == "1"
        expect(cart_page.get_item_price_element(products["backpack"]["name"])).to_have_text(
            f"${products['backpack']['price']}"
        )

    def test_tc02_display_empty_cart(self, page: Page):
        login_as_standard_user(page)
        cart_page = CartPage(page)
        cart_page.goto()

        expect(cart_page.page_title).to_have_text("Your Cart")
        expect(cart_page.cart_items).to_have_count(0)
        expect(cart_page.continue_shopping_button).to_be_visible()

    def test_tc03_remove_item_from_cart(self, page: Page):
        cart_page = prepare_cart_with_item(page, products["backpack"]["name"])
        cart_page.remove_item(products["backpack"]["name"])

        expect(cart_page.cart_items).to_have_count(0)
        expect(cart_page.shopping_cart_badge).not_to_be_visible()

    def test_tc04_display_two_products_in_cart(self, page: Page):
        inventory_page = login_as_standard_user(page)
        inventory_page.add_product_to_cart(products["backpack"]["name"])
        inventory_page.add_product_to_cart(products["bikeLight"]["name"])
        inventory_page.go_to_cart()

        cart_page = CartPage(page)
        item_names = cart_page.get_cart_item_names()
        assert products["backpack"]["name"] in item_names
        assert products["bikeLight"]["name"] in item_names
        expect(cart_page.cart_items).to_have_count(2)
        expect(cart_page.get_item_remove_button(products["backpack"]["name"])).to_have_text(
            "Remove"
        )
        expect(cart_page.get_item_remove_button(products["bikeLight"]["name"])).to_have_text(
            "Remove"
        )

    def test_tc05_continue_shopping_from_cart(self, page: Page):
        cart_page = prepare_cart_with_item(page, products["backpack"]["name"])
        inventory_page = cart_page.continue_shopping()

        expect(inventory_page.page_title).to_have_text("Products")
        expect(inventory_page.shopping_cart_badge).to_have_text("1")

    def test_tc06_checkout_from_cart(self, page: Page):
        cart_page = prepare_cart_with_item(page, products["backpack"]["name"])
        checkout_info_page = cart_page.proceed_to_checkout()

        expect(checkout_info_page.page_title).to_have_text("Checkout: Your Information")
        expect(checkout_info_page.first_name_input).to_be_visible()
        expect(checkout_info_page.last_name_input).to_be_visible()
        expect(checkout_info_page.postal_code_input).to_be_visible()
