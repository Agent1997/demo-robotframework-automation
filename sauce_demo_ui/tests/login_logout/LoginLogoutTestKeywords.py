from SeleniumLibrary import SeleniumLibrary
from robot.api.deco import library, keyword

from sauce_demo_ui.page_objects import SauceDemoApp


@library(scope='GLOBAL')
class LoginLogoutTestKeywords:

    def __init__(self, headless: bool = True):
        self.app = SauceDemoApp(SeleniumLibrary())
        self.is_headless = headless

    @keyword
    def open_sauce_lab_demo_app(self):
        self.app.browser.open_sauce_demo_app(headless=self.is_headless)

    @keyword
    def close_sauce_lab_demo_app(self):
        self.app.browser.close_sauce_demo_app()

    @keyword
    def user_login_to_sauce_lab_demo_app(self, username: str, password: str):
        self.app.login.login(username=username, password=password)

    @keyword
    def user_should_not_be_able_to_login(self):
        self.app.login.LOGIN_BTN.should_be_visible()

    @keyword
    def error_message_should_be(self, exp_err_msg: str):
        self.app.login.ERROR_MESSAGE.text_should_be(exp_text=exp_err_msg)

    @keyword
    def user_should_be_in_the_product_page_upon_successful_login(self):
        self.app.products.PAGE_TITLE.should_be_visible()

    @keyword
    def reload_sauce_demo_app(self):
        self.app.browser.reload()

    @keyword
    def user_logout_from_sauce_lab_demo_app(self):
        self.app.menu.open()
        self.app.menu.LOGOUT_BTN.click()

    @keyword
    def user_should_be_in_the_login_page_upon_successful_logout(self):
        self.app.login.LOGIN_BTN.should_be_visible()