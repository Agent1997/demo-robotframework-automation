from SeleniumLibrary import SeleniumLibrary

from autocore.web.element import WebElementFactory
from autocore.web.webactions import WebActions
from sauce_demo_ui.timeouts import LOGIN_PAGE_TIMEOUT

USERNAME_FLD: str = 'id:user-name'
PASSWORD_FLD: str = 'id:password'
LOGIN_BTN: str = 'id:login-button'
ERROR_DISPLAY: str = 'xpath://h3[@data-test="error"]'


class LoginPage:

    def __init__(self, se_lib: SeleniumLibrary):
        self.__wa = WebActions(ctx=se_lib, timeout=LOGIN_PAGE_TIMEOUT)
        self.__element = WebElementFactory(ctx=se_lib, timeout=LOGIN_PAGE_TIMEOUT)

    @property
    def ERROR_MESSAGE(self):
        return self.__element.with_locator(locator=ERROR_DISPLAY)

    @property
    def LOGIN_BTN(self):
        return self.__element.with_locator(locator=LOGIN_BTN)

    def login(self, username: str, password: str):
        if len(username) > 0:
            self.__wa.input_text(locator=USERNAME_FLD, text=username)
        if len(password) > 0:
            self.__wa.input_text(locator=PASSWORD_FLD, text=password)
        self.__wa.click(locator=LOGIN_BTN)
