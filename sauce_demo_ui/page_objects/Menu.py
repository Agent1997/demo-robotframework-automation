from datetime import timedelta

from SeleniumLibrary import SeleniumLibrary

from autocore.web.element import WebElementFactory
from autocore.web.webactions import WebActions

BURGER_MENU_BTN: str = 'id:react-burger-menu-btn'
CLOSE_MENU_BTN: str = 'id:react-burger-cross-btn'
ALL_ITEMS_MENU_OPTION: str = 'id:inventory_sidebar_link'
ABOUT_MENU_OPTION: str = 'id:about_sidebar_link'
LOGOUT_BTN: str = 'id:logout_sidebar_link'


class Menu:

    def __init__(self, se_lib: SeleniumLibrary):
        self.__wa = WebActions(ctx=se_lib)
        self.__element = WebElementFactory(ctx=se_lib)

    @property
    def LOGOUT_BTN(self):
        return self.__element.with_locator(locator=LOGOUT_BTN)

    def open(self):
        if self.__wa.is_visible(locator=BURGER_MENU_BTN, timeout=timedelta(seconds=5)):
            self.__wa.click(locator=BURGER_MENU_BTN)
            self.__wa.wait_until_visible(locator=CLOSE_MENU_BTN)
