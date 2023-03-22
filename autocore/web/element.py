from datetime import timedelta

from SeleniumLibrary import SeleniumLibrary

from autocore.web.webactions import WebActions


class WebElementFactory:

    def __init__(self, ctx: SeleniumLibrary, timeout: timedelta = timedelta(seconds=5), screenshot: bool = False):
        self.__ctx = ctx
        self.__timeout = timeout
        self.__screenshot = screenshot

    def with_locator(self, locator: str):
        return _WebElement(locator=locator, ctx=self.__ctx, timeout=self.__timeout, screenshot=self.__screenshot)


class _WebElement:

    def __init__(self, locator: str, ctx: SeleniumLibrary, timeout: timedelta = timedelta(seconds=5),
                 screenshot: bool = False):
        self.__wa = WebActions(ctx=ctx, timeout=timeout, screenshot=screenshot)
        self.__locator = locator

    @property
    def locator(self):
        return self.__locator

    def attribute_ends_with(self, attribute: str, exp_value: str) -> bool:
        return self.__wa.attribute_ends_with(locator=self.__locator, attribute=attribute, exp_value=exp_value)

    def attribute_contains(self, attribute: str, exp_value: str) -> bool:
        return self.__wa.attribute_contains(locator=self.__locator, attribute=attribute, exp_value=exp_value)

    def attribute_value_should_be(self, attribute: str, exp_value: str):
        self.__wa.attribute_value_should_be(locator=self.__locator, attribute=attribute, exp_value=exp_value)

    def attribute_value_should_end_with(self, attribute: str, exp_value: str):
        self.__wa.attribute_value_should_end_with(locator=self.__locator, attribute=attribute, exp_value=exp_value)

    def attribute_value_should_start_with(self, attribute: str, exp_value: str):
        self.__wa.attribute_value_should_start_with(locator=self.__locator, attribute=attribute, exp_value=exp_value)

    def attribute_value_should_contain(self, attribute: str, exp_value: str):
        self.__wa.attribute_value_should_contain(locator=self.__locator, attribute=attribute, exp_value=exp_value)

    def click(self):
        self.__wa.click(locator=self.__locator)

    def count(self) -> int:
        return self.__wa.count(locator=self.__locator)

    def count_should_be(self, exp_count: str):
        self.__wa.count_of_should_be(locator=self.__locator, exp_count=exp_count)

    def delete_text_via_keys(self):
        self.__wa.delete_text_via_keys(locator=self.__locator)

    def double_click(self):
        self.__wa.double_click(locator=self.__locator)

    def get_attribute(self, attribute: str) -> str:
        return self.__wa.get_attribute(locator=self.__locator, attribute=attribute)

    def get_text(self) -> str:
        return self.__wa.get_text(locator=self.__locator)

    def get_texts(self) -> list[str]:
        return self.__wa.get_texts(locator=self.__locator)

    def get_value(self) -> str:
        return self.__wa.get_value(locator=self.__locator)

    def get_values(self):
        return self.__wa.get_values(locator=self.__locator)

    def input_text(self, text: str, click: bool = True, press_enter: bool = False, clear: bool = True):
        self.__wa.input_text(locator=self.__locator, text=text, click=click, press_enter=press_enter, clear=clear)

    def input_password(self, password: str, click: bool = True, press_enter: bool = False, clear: bool = True):
        self.__wa.input_password(locator=self.__locator, password=password, click=click, press_enter=press_enter,
                                 clear=clear)

    def is_text(self, exp_text: str, ignore_case: bool = False, ignore_space: bool = False,
                timeout: timedelta = None) -> bool:
        return self.__wa.is_text(locator=self.__locator, exp_text=exp_text, ignore_case=ignore_case,
                                 ignore_space=ignore_space, timeout=timeout)

    def is_value(self, exp_value: str, ignore_case: bool = False, ignore_space: bool = False) -> bool:
        return self.__wa.is_value(locator=self.__locator, exp_value=exp_value, ignore_case=ignore_case,
                                  ignore_space=ignore_space)

    def is_visible(self, timeout: timedelta = None) -> bool:
        return self.__wa.is_visible(locator=self.__locator, timeout=timeout)

    def is_enabled(self, timeout: timedelta = None) -> bool:
        return self.__wa.is_enabled(locator=self.__locator, timeout=timeout)

    def is_selected(self) -> bool:
        return self.__wa.is_selected(locator=self.__locator)

    def press_enter(self):
        self.__wa.press_enter(locator=self.__locator)

    def scroll_into_view(self):
        self.__wa.scroll_into_view(locator=self.__locator)

    def should_be_visible(self, timeout: timedelta = None):
        self.__wa.should_be_visible(locator=self.__locator, timeout=timeout)

    def should_not_be_visible(self, timeout: timedelta = None):
        self.__wa.should_not_be_visible(locator=self.__locator, timeout=timeout)

    def should_be_enabled(self, timeout: timedelta = timedelta(seconds=0.5)):
        self.__wa.should_be_enabled(locator=self.__locator, timeout=timeout)

    def should_be_selected(self):
        self.__wa.should_be_selected(locator=self.__locator)

    def should_not_be_selected(self):
        self.__wa.should_not_be_selected(locator=self.__locator)

    def should_be_disabled(self):
        self.__wa.should_be_disabled(locator=self.__locator)

    def text_should_be(self, exp_text: str, ignore_case: bool = False, ignore_space: bool = False,
                       with_wait: bool = False, strip: bool = False):
        self.__wa.text_should_be(locator=self.__locator, exp_text=exp_text, ignore_case=ignore_case,
                                 ignore_space=ignore_space, with_wait=with_wait, strip=strip)

    def text_should_be_empty(self):
        self.__wa.text_should_be_empty(locator=self.__locator)

    def text_should_contain(self, exp_text: str, ignore_case: bool = False, ignore_space: bool = False):
        self.__wa.text_should_contain(locator=self.__locator, exp_text=exp_text, ignore_case=ignore_case,
                                      ignore_space=ignore_space)

    def text_should_start_with(self, exp_text: str, ignore_case: bool = False, ignore_space: bool = False):
        self.__wa.text_should_start_with(locator=self.__locator, exp_text=exp_text, ignore_case=ignore_case,
                                         ignore_space=ignore_space)

    def text_should_end_with(self, exp_text: str, ignore_case: bool = False, ignore_space: bool = False):
        self.__wa.text_should_end_with(locator=self.__locator, exp_text=exp_text, ignore_case=ignore_case,
                                       ignore_space=ignore_space)

    def text_should_not_be_empty(self):
        self.__wa.text_should_not_be_empty(locator=self.__locator)

    def texts_should_contain(self, exp_text: str):
        self.__wa.texts_should_contain(locator=self.__locator, exp_text=exp_text)

    def type_number(self, number: str):
        self.__wa.type_number(locator=self.__locator, number=number)

    def value_should_be(self, exp_value: str, ignore_case: bool = False, ignore_space: bool = False):
        self.__wa.value_should_be(locator=self.__locator, exp_value=exp_value, ignore_case=ignore_case,
                                  ignore_space=ignore_space)

    def value_should_be_empty(self):
        self.__wa.value_should_be_empty(locator=self.__locator)

    def value_should_not_be_empty(self):
        self.__wa.value_should_not_be_empty(locator=self.__locator)

    def value_should_contain(self, exp_text: str, ignore_case: bool = False, ignore_space: bool = False):
        self.__wa.value_should_contain(locator=self.__locator, exp_text=exp_text, ignore_case=ignore_case,
                                       ignore_space=ignore_space)

    def value_should_start_with(self, exp_text: str, ignore_case: bool = False, ignore_space: bool = False):
        self.__wa.value_should_start_with(locator=self.__locator, exp_text=exp_text, ignore_case=ignore_case,
                                          ignore_space=ignore_space)

    def value_should_end_with(self, exp_text: str, ignore_case: bool = False, ignore_space: bool = False):
        self.__wa.value_should_end_with(locator=self.__locator, exp_text=exp_text, ignore_case=ignore_case,
                                        ignore_space=ignore_space)

    def wait_until_attribute_value_contains(self, attribute: str, exp_value: str, timeout: timedelta = None) -> str:
        return self.__wa.wait_until_attribute_value_contains(locator=self.__locator, attribute=attribute,
                                                             exp_value=exp_value, timeout=timeout)

    def wait_until_count_is_greater_than(self, count: int, timeout: timedelta = None) -> int:
        return self.__wa.wait_until_count_is_greater_than(locator=self.__locator, count=count, timeout=timeout)

    def wait_until_text_is(self, exp_text: str, ignore_case: bool = False, ignore_space: bool = False,
                           timeout: timedelta = None) -> str:
        return self.__wa.wait_until_text_is(locator=self.__locator, exp_text=exp_text, ignore_case=ignore_case,
                                            ignore_space=ignore_space, timeout=timeout)

    def wait_until_text_is_not_empty(self, timeout: timedelta = None) -> str:
        return self.__wa.wait_until_text_is_not_empty(locator=self.__locator, timeout=timeout)

    def wait_until_found(self, timeout: timedelta = None):
        self.__wa.wait_until_found(locator=self.__locator, timeout=timeout)

    def wait_until_value_is_not_empty(self, timeout: timedelta = None):
        self.__wa.wait_until_value_is_not_empty(locator=self.__locator, timeout=timeout)

    def wait_until_value_is(self, exp_value: str, ignore_case: bool = False, ignore_space: bool = False,
                            timeout: timedelta = None):
        self.__wa.wait_until_value_is(locator=self.__locator, exp_value=exp_value, ignore_case=ignore_case,
                                      ignore_space=ignore_space, timeout=timeout)

    def wait_until_visible(self, timeout: timedelta = None):
        self.__wa.wait_until_visible(locator=self.__locator, timeout=timeout)

    def wait_until_interactible(self, timeout: timedelta = None):
        self.__wa.wait_until_interactible(locator=self.__locator, timeout=timeout)

    def wait_until_not_visible(self, timeout: timedelta = None):
        self.__wa.wait_until_not_visible(locator=self.__locator, timeout=timeout)

    def wait_until_enabled(self, timeout: timedelta = None):
        self.__wa.wait_until_enabled(locator=self.__locator, timeout=timeout)
