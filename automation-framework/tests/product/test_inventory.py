from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.login_page import LoginPage
from data.loader import load_json
from workflows import login_as_standard_user

products = load_json("products.json")


class TestInventory:
    def test_tc01_display_six_products(self, page: Page):
        inventory_page = login_as_standard_user(page)

        expect(inventory_page.page_title).to_have_text("Products")
        expect(inventory_page.inventory_items).to_have_count(6)

        product_names = inventory_page.get_product_names()
        assert product_names == products["allProducts"]
        inventory_page.verify_product_list_layout()

    def test_tc02_sort_by_name_za(self, page: Page):
        inventory_page = login_as_standard_user(page)
        inventory_page.sort_by("za")

        names = inventory_page.get_product_names()
        assert names[0] == products["redTShirt"]["name"]

    def test_tc03_sort_by_price_low_to_high(self, page: Page):
        inventory_page = login_as_standard_user(page)
        inventory_page.sort_by("lohi")

        names = inventory_page.get_product_names()
        assert names[0] == products["onesie"]["name"]

        prices = inventory_page.get_product_prices()
        for i in range(1, len(prices)):
            assert prices[i] >= prices[i - 1]

    def test_tc04_sort_by_price_high_to_low(self, page: Page):
        inventory_page = login_as_standard_user(page)
        inventory_page.sort_by("hilo")

        names = inventory_page.get_product_names()
        assert names[0] == products["fleeceJacket"]["name"]

        prices = inventory_page.get_product_prices()
        for i in range(1, len(prices)):
            assert prices[i] <= prices[i - 1]

    def test_tc05_add_product_to_cart(self, page: Page):
        inventory_page = login_as_standard_user(page)
        inventory_page.add_product_to_cart(products["backpack"]["name"])

        expect(inventory_page.get_add_to_cart_button(products["backpack"]["name"])).to_have_text(
            "Remove"
        )
        expect(inventory_page.shopping_cart_badge).to_be_visible()
        expect(inventory_page.shopping_cart_badge).to_have_text("1")

    def test_tc06_add_two_products_to_cart(self, page: Page):
        inventory_page = login_as_standard_user(page)
        inventory_page.add_product_to_cart(products["backpack"]["name"])
        inventory_page.add_product_to_cart(products["bikeLight"]["name"])

        expect(inventory_page.get_add_to_cart_button(products["backpack"]["name"])).to_have_text(
            "Remove"
        )
        expect(inventory_page.get_add_to_cart_button(products["bikeLight"]["name"])).to_have_text(
            "Remove"
        )
        expect(inventory_page.shopping_cart_badge).to_have_text("2")

    def test_tc07_remove_product_from_cart(self, page: Page):
        inventory_page = login_as_standard_user(page)
        inventory_page.add_product_to_cart(products["backpack"]["name"])
        inventory_page.remove_product_from_cart(products["backpack"]["name"])

        expect(inventory_page.get_add_to_cart_button(products["backpack"]["name"])).to_have_text(
            "Add to cart"
        )
        expect(inventory_page.shopping_cart_badge).not_to_be_visible()

    def test_tc08_open_product_detail(self, page: Page):
        inventory_page = login_as_standard_user(page)
        product_detail_page = inventory_page.open_product_detail_page(products["backpack"]["name"])

        expect(product_detail_page.product_name).to_have_text(products["backpack"]["name"])

    def test_tc09_logout_from_inventory(self, page: Page):
        inventory_page = login_as_standard_user(page)
        inventory_page.logout()

        login_page = LoginPage(page)
        expect(login_page.page).to_have_url("/")
        expect(login_page.login_button).to_be_visible()

    def test_tc10_open_cart_from_inventory(self, page: Page):
        inventory_page = login_as_standard_user(page)
        inventory_page.add_product_to_cart(products["backpack"]["name"])
        inventory_page.go_to_cart()

        cart_page = CartPage(page)
        expect(cart_page.page_title).to_have_text("Your Cart")
        expect(cart_page.get_cart_item_by_name(products["backpack"]["name"])).to_be_visible()

    def test_tc11_reset_app_state(self, page: Page):
        inventory_page = login_as_standard_user(page)
        inventory_page.add_product_to_cart(products["backpack"]["name"])
        expect(inventory_page.shopping_cart_badge).to_be_visible()

        inventory_page.reset_app_state()

        expect(inventory_page.get_add_to_cart_button(products["backpack"]["name"])).to_have_text(
            "Add to cart", timeout=10_000
        )
        expect(inventory_page.shopping_cart_badge).not_to_be_visible()
