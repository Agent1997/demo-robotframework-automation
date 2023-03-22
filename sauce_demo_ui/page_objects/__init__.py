from SeleniumLibrary import SeleniumLibrary

from sauce_demo_ui.page_objects.Browser import Browser
from sauce_demo_ui.page_objects.Login import LoginPage
from sauce_demo_ui.page_objects.Products import Products


class SauceDemoApp:

    def __init__(self, se_lib: SeleniumLibrary):
        self.__se_lib = se_lib
        self.__browser = Browser(se_lib=se_lib)
        self.__login = LoginPage(se_lib=se_lib)
        self.__products = Products(se_lib=se_lib)

    @property
    def browser(self):
        return self.__browser

    @property
    def login(self):
        return self.__login

    @property
    def products(self):
        return self.__products
