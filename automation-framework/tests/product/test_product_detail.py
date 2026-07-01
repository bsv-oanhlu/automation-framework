from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from data.loader import load_json
from workflows import prepare_product_detail_page

products = load_json("products.json")


class TestProductDetail:
    def test_tc01_display_backpack_detail(self, page: Page):
        product_detail_page = prepare_product_detail_page(page, products["backpack"]["name"])

        expect(product_detail_page.product_image).to_be_visible()
        expect(product_detail_page.product_name).to_have_text(products["backpack"]["name"])
        expect(product_detail_page.product_description).to_be_visible()
        expect(product_detail_page.product_price).to_have_text(f"${products['backpack']['price']}")
        expect(product_detail_page.add_to_cart_button).to_have_text("Add to cart")
        expect(product_detail_page.back_to_products_link).to_be_visible()

    def test_tc02_add_to_cart_from_detail(self, page: Page):
        product_detail_page = prepare_product_detail_page(page, products["backpack"]["name"])
        product_detail_page.add_to_cart()

        expect(product_detail_page.add_to_cart_button).to_have_text("Remove")
        expect(product_detail_page.shopping_cart_badge).to_be_visible()
        expect(product_detail_page.shopping_cart_badge).to_have_text("1")

    def test_tc03_remove_from_cart_from_detail(self, page: Page):
        product_detail_page = prepare_product_detail_page(page, products["backpack"]["name"])
        product_detail_page.add_to_cart()
        product_detail_page.remove_from_cart()

        expect(product_detail_page.add_to_cart_button).to_have_text("Add to cart")
        expect(product_detail_page.shopping_cart_badge).not_to_be_visible()

    def test_tc04_back_to_products(self, page: Page):
        product_detail_page = prepare_product_detail_page(page, products["backpack"]["name"])
        inventory_page = product_detail_page.back_to_products()

        expect(inventory_page.page_title).to_have_text("Products")
        expect(inventory_page.inventory_items).to_have_count(6)

    def test_tc05_display_bike_light_detail(self, page: Page):
        product_detail_page = prepare_product_detail_page(page, products["bikeLight"]["name"])

        expect(product_detail_page.product_name).to_have_text(products["bikeLight"]["name"])
        expect(product_detail_page.product_price).to_have_text(
            f"${products['bikeLight']['price']}"
        )
        expect(product_detail_page.product_description).to_be_visible()

    def test_tc06_open_cart_from_product_detail(self, page: Page):
        product_detail_page = prepare_product_detail_page(page, products["backpack"]["name"])
        product_detail_page.add_to_cart()
        product_detail_page.go_to_cart()

        cart_page = CartPage(page)
        expect(cart_page.page_title).to_have_text("Your Cart")
        expect(cart_page.get_cart_item_by_name(products["backpack"]["name"])).to_be_visible()
        expect(cart_page.get_item_price_element(products["backpack"]["name"])).to_have_text(
            f"${products['backpack']['price']}"
        )
