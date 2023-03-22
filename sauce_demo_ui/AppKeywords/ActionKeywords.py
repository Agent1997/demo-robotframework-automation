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