from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from data.loader import get_user_from_csv
from workflows import login_with_credentials, users


class TestLogin:
    def test_tc01_login_ui_display(self, page: Page):
        login_page = LoginPage(page)
        login_page.goto()

        expect(login_page.logo).to_be_visible()
        expect(login_page.username_input).to_be_visible()
        expect(login_page.password_input).to_be_visible()
        expect(login_page.login_button).to_be_visible()
        expect(login_page.login_credentials).to_be_visible()
        expect(login_page.login_password_hint).to_be_visible()

    def test_tc02_login_success_standard_user(self, page: Page):
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(users["validUser"]["username"], users["validUser"]["password"])

        inventory_page = login_page.wait_for_inventory_page()
        expect(inventory_page.page_title).to_have_text("Products")
        expect(inventory_page.inventory_items).to_have_count(6)

    def test_tc03_login_fail_wrong_password(self, page: Page):
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(
            users["invalidPassword"]["username"],
            users["invalidPassword"]["password"],
        )

        expect(login_page.error_message).to_be_visible()
        expect(login_page.error_message).to_have_text(
            "Epic sadface: Username and password do not match any user in this service"
        )
        expect(login_page.page).to_have_url("/")

    def test_tc04_login_fail_empty_username(self, page: Page):
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login("", users["validUser"]["password"])

        expect(login_page.error_message).to_be_visible()
        expect(login_page.error_message).to_have_text("Epic sadface: Username is required")
        expect(login_page.page).to_have_url("/")

    def test_tc05_login_fail_empty_password(self, page: Page):
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(users["validUser"]["username"], "")

        expect(login_page.error_message).to_be_visible()
        expect(login_page.error_message).to_have_text("Epic sadface: Password is required")
        expect(login_page.page).to_have_url("/")

    def test_tc06_login_fail_locked_out_user(self, page: Page):
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(
            users["lockedOutUser"]["username"],
            users["lockedOutUser"]["password"],
        )

        expect(login_page.error_message).to_be_visible()
        expect(login_page.error_message).to_have_text(
            "Epic sadface: Sorry, this user has been locked out."
        )
        expect(login_page.page).to_have_url("/")

    def test_tc07_login_success_problem_user(self, page: Page):
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(
            users["problemUser"]["username"],
            users["problemUser"]["password"],
        )

        inventory_page = login_page.wait_for_inventory_page()
        expect(inventory_page.page_title).to_have_text("Products")

    def test_tc08_login_success_performance_glitch_user(self, page: Page):
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(
            users["performanceGlitchUser"]["username"],
            users["performanceGlitchUser"]["password"],
        )

        inventory_page = login_page.wait_for_inventory_page(timeout=30_000)
        expect(inventory_page.page_title).to_have_text("Products")

    def test_tc09_login_with_csv_data(self, page: Page):
        csv_user = get_user_from_csv("Valid user with full access")
        assert csv_user is not None

        login_with_credentials(page, csv_user["username"], csv_user["password"])
        inventory_page = LoginPage(page).wait_for_inventory_page()
        expect(inventory_page.inventory_items).to_have_count(6)
