from SeleniumLibrary import SeleniumLibrary

from autocore.web.BroswerConfig import chrome_options
from autocore.web.webactions import WebActions


class Browser:

    def __init__(self, se_lib: SeleniumLibrary):
        self.__wa = WebActions(ctx=se_lib)

    def open_sauce_demo_app(self, headless: bool):
        options = chrome_options(is_headless=headless)
        self.__wa.open_browser(url='https://www.saucedemo.com/', browser='chrome', options=options, alias=None)

    def close_sauce_demo_app(self):
        self.__wa.close_all_browsers()

    def reload(self):
        self.__wa.reload_browser()
