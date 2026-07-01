import re

from playwright.sync_api import Page, expect

from data.loader import load_json
from workflows import checkout_data, prepare_checkout_info_page

products = load_json("products.json")
checkout = load_json("checkout.json")


class TestCheckoutInfo:
    def test_tc01_display_checkout_info_page(self, page: Page):
        checkout_info_page = prepare_checkout_info_page(page, products["backpack"]["name"])

        expect(checkout_info_page.page_title).to_have_text("Checkout: Your Information")
        expect(checkout_info_page.first_name_input).to_be_visible()
        expect(checkout_info_page.last_name_input).to_be_visible()
        expect(checkout_info_page.postal_code_input).to_be_visible()
        expect(checkout_info_page.cancel_button).to_be_visible()
        expect(checkout_info_page.continue_button).to_be_visible()

    def test_tc02_fill_valid_info_and_continue(self, page: Page):
        checkout_info_page = prepare_checkout_info_page(page, products["backpack"]["name"])
        info = checkout_data["validInfo"]

        checkout_info_page.fill_checkout_info(
            info["firstName"], info["lastName"], info["postalCode"]
        )
        overview_page = checkout_info_page.submit_and_continue()

        expect(overview_page.page_title).to_have_text("Checkout: Overview")

    def test_tc03_error_when_all_fields_empty(self, page: Page):
        checkout_info_page = prepare_checkout_info_page(page, products["backpack"]["name"])
        checkout_info_page.submit()

        expect(checkout_info_page.error_message).to_be_visible()
        expect(checkout_info_page.error_message).to_have_text(
            checkout["errorMessages"]["firstNameRequired"]
        )
        expect(checkout_info_page.page).to_have_url(re.compile("checkout-step-one"))

    def test_tc04_error_when_missing_last_name(self, page: Page):
        checkout_info_page = prepare_checkout_info_page(page, products["backpack"]["name"])
        checkout_info_page.fill_checkout_info("Nguyen", "", "")
        checkout_info_page.submit()

        expect(checkout_info_page.error_message).to_be_visible()
        expect(checkout_info_page.error_message).to_have_text(
            checkout["errorMessages"]["lastNameRequired"]
        )
        expect(checkout_info_page.page).to_have_url(re.compile("checkout-step-one"))

    def test_tc05_error_when_missing_postal_code(self, page: Page):
        checkout_info_page = prepare_checkout_info_page(page, products["backpack"]["name"])
        checkout_info_page.fill_checkout_info("Nguyen", "Van A", "")
        checkout_info_page.submit()

        expect(checkout_info_page.error_message).to_be_visible()
        expect(checkout_info_page.error_message).to_have_text(
            checkout["errorMessages"]["postalCodeRequired"]
        )
        expect(checkout_info_page.page).to_have_url(re.compile("checkout-step-one"))

    def test_tc06_cancel_checkout_back_to_cart(self, page: Page):
        checkout_info_page = prepare_checkout_info_page(page, products["backpack"]["name"])
        cart_page = checkout_info_page.cancel()

        expect(cart_page.page_title).to_have_text("Your Cart")
        expect(cart_page.cart_items).to_have_count(1)
