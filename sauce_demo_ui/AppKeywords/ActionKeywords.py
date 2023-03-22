from SeleniumLibrary import SeleniumLibrary
from robot.api.deco import keyword

from sauce_demo_ui.page_objects import SauceDemoApp


class ActionKeywords:

    def __init__(self, se_lib: SeleniumLibrary):
        self.app = SauceDemoApp(se_lib=se_lib)

    @keyword
    def user_logout_from_sauce_lab_demo_app(self):
        self.app.menu.open()
        self.app.menu.LOGOUT_BTN.click()

    @keyword
    def user_login_to_sauce_lab_demo_app(self, username: str, password: str):
        self.app.login.login(username=username, password=password)

    @keyword
    def user_sorted_the_products_by_name_a_to_z(self):
        self.app.products.sort_by_select_value('az')

    @keyword
    def user_sorted_the_products_by_name_z_to_a(self):
        self.app.products.sort_by_select_value('za')

    @keyword
    def user_sorted_the_products_by_price_low_to_high(self):
        self.app.products.sort_by_select_value('lohi')

    @keyword
    def user_sorted_the_products_by_price_high_to_low(self):
        self.app.products.sort_by_select_value('hilo')

