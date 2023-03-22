from SeleniumLibrary import SeleniumLibrary
from robot.api.deco import keyword

from sauce_demo_ui.page_objects import SauceDemoApp


class BrowserKeywords:

    def __init__(self, se_lib: SeleniumLibrary, headless: bool = True):
        self.app = SauceDemoApp(se_lib=se_lib)
        self.is_headless = headless

    @keyword
    def open_sauce_lab_demo_app(self):
        self.app.browser.open_sauce_demo_app(headless=self.is_headless)

    @keyword
    def close_sauce_lab_demo_app(self):
        self.app.browser.close_sauce_demo_app()

    @keyword
    def reload_sauce_demo_app(self):
        self.app.browser.reload()
