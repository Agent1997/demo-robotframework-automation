from SeleniumLibrary import SeleniumLibrary
from robot.api.deco import keyword

from sauce_demo_ui.page_objects import SauceDemoApp


class ValidationKeywords:

    def __init__(self, se_lib: SeleniumLibrary):
        self.app = SauceDemoApp(se_lib=se_lib)

    @keyword
    def user_should_be_in_the_login_page_upon_successful_logout(self):
        self.app.login.LOGIN_BTN.should_be_visible()

    @keyword
    def user_should_not_be_able_to_login(self):
        self.app.login.LOGIN_BTN.should_be_visible()

    @keyword
    def login_error_message_should_be(self, exp_err_msg: str):
        self.app.login.ERROR_MESSAGE.text_should_be(exp_text=exp_err_msg)

    @keyword
    def user_should_be_in_the_product_page_upon_successful_login(self):
        self.app.products.PAGE_TITLE.should_be_visible()
