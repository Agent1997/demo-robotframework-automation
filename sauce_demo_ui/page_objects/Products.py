from SeleniumLibrary import SeleniumLibrary

from autocore.web.element import WebElementFactory
from autocore.web.webactions import WebActions
from sauce_demo_ui.timeouts import PRODUCT_PAGE_TIMEOUT

APP_LOGO: str = 'xpath://div[@class="app_logo"]'
SELECT_PRODUCT_SORT: str = 'xpath://select[@class="product_sort_container"]'
ADD_TO_CART_BTN_TPL: str = 'xpath://div[normalize-space()="{0}"]/../../..//button'  # parameter is complete item name
ITEM_PRICE_TPL: str = 'xpath://div[normalize-space()="{0}"]/../../..//div[@class="inventory_item_price"]'  # parameter is complete item name
ITEM_DESCRIPTION: str = 'xpath:////div[normalize-space()="{0}"]//../following-sibling::div[@class="inventory_item_desc"]'  # parameter is complete item name
PAGE_TITLE: str = 'xpath://span[contains(text(),"Products")]'


class Products:

    def __init__(self, se_lib: SeleniumLibrary):
        self.__wa = WebActions(ctx=se_lib, timeout=PRODUCT_PAGE_TIMEOUT)
        self.__element = WebElementFactory(ctx=se_lib, timeout=PRODUCT_PAGE_TIMEOUT)

    @property
    def PAGE_TITLE(self):
        return self.__element.with_locator(locator=PAGE_TITLE)

    def sort_by_select_value(self, select_value: str):
        self.__wa.select_by_value(locator=SELECT_PRODUCT_SORT, value=select_value)
