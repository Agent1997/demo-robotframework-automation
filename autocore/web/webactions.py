import random
import time
import traceback
from datetime import timedelta

from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.errors import ElementNotFound
from robot.api import logger
from selenium.common import ElementNotInteractableException, ElementClickInterceptedException, \
    StaleElementReferenceException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from autocore.asserts import assert_equal, assert_that_text_ends_with, assert_that_text_starts_with, \
    assert_that_text_contains, assert_that_text_is_not_empty, assert_that_list_contains_all, assert_true, assert_false, \
    assert_that_list_has_item


def sleep(seconds: float = 0):
    """Pause execution in seconds."""
    if seconds < 0:
        seconds = 0

    # time.sleep can't be stopped in windows
    # to ensure that we can signal stop (with timeout)
    # split sleeping to small pieces
    # reference: robot BuiltIn().sleep()
    end_time = time.time() + seconds
    while True:
        remaining = end_time - time.time()
        if remaining <= 0:
            break
        time.sleep(min(remaining, 0.01))


def _transform(text: str, remove_case: bool = False, remove_spaces: bool = False, strip: bool = False) -> str:
    """Transform the text by converting to lowercase and/or removing spaces."""
    if remove_case:
        text = text.lower()
    if remove_spaces:
        text = text.replace(" ", "").strip()
    if strip:
        text = text.strip()
    return text


def _get_retry_count(timeout: timedelta) -> int:
    """Return the retry count based on the timeout provided."""
    if timeout is None:
        raise Exception("Timeout can not be None.")

    timeout = timeout.total_seconds()
    if timeout < 1:
        return 1
    elif 1 <= timeout < 5:
        return 5
    elif 5 <= timeout < 10:
        return 10
    elif 10 <= timeout < 20:
        return 20
    elif 20 <= timeout < 30:
        return 25
    else:
        return 45


def _click_number(el: WebElement, number: str):
    """Type the number to the element via keys. Period (.) is in accepted for decimal points."""
    if number == "0":
        el.send_keys(Keys.NUMPAD0)
    elif number == "1":
        el.send_keys(Keys.NUMPAD1)
    elif number == "2":
        el.send_keys(Keys.NUMPAD2)
    elif number == "3":
        el.send_keys(Keys.NUMPAD3)
    elif number == "4":
        el.send_keys(Keys.NUMPAD4)
    elif number == "5":
        el.send_keys(Keys.NUMPAD5)
    elif number == "6":
        el.send_keys(Keys.NUMPAD6)
    elif number == "7":
        el.send_keys(Keys.NUMPAD7)
    elif number == "8":
        el.send_keys(Keys.NUMPAD8)
    elif number == "9":
        el.send_keys(Keys.NUMPAD9)
    elif number == ".":
        el.send_keys(Keys.DECIMAL)


def _random_item(lst, except_for=None):
    if except_for is None:
        return random.choice(lst)
    else:
        rule = random.choice(lst)
        if rule.strip().lower() == except_for.strip().lower():
            i = lst.index(rule)

            if i != 0:
                rule = lst[0]
            elif i != len(lst) - 1:
                rule = lst[-1]

        return rule


class WebActions:

    def __init__(self, ctx: SeleniumLibrary, timeout: timedelta = timedelta(seconds=5), screenshot: bool = False):
        self.__ctx = ctx
        self.__timeout = timeout
        self.__screenshot = screenshot

    def attribute_ends_with(self, locator: str, attribute: str, exp_value: str) -> bool:
        """Returns True if attribute of the element ends with the exp value, otherwise false."""
        return self.get_attribute(locator=locator, attribute=attribute).endswith(exp_value)

    def attribute_contains(self, locator: str, attribute: str, exp_value: str) -> bool:
        """Returns True if attribute of the element contains the exp value, otherwise false."""
        return exp_value in self.get_attribute(locator=locator, attribute=attribute)

    def attribute_value_should_be(self, locator: str, attribute: str, exp_value: str):
        """Verify that the attribute of the element match the exp value, raises AssertionError if not."""
        act = self.get_attribute(locator=locator, attribute=attribute)
        assert_equal(act, exp_value,
                     f"Expecting value of '{attribute}' attribute of element located by '{locator}' to be {exp_value} but got {act}.",
                     s_msg=f"Verified attribute '{attribute}' of element located by '{locator}' is {exp_value}. Actual: {act}.")

    def attribute_value_should_end_with(self, locator: str, attribute: str, exp_value: str):
        """Verify that the attribute of the element ends with the exp value, raises AssertionError if not."""
        act = self.get_attribute(locator=locator, attribute=attribute)
        assert_that_text_ends_with(act, exp_value,
                                   f"Expecting value of '{attribute}' attribute of element located by '{locator}' to end with {exp_value} but got {act}.",
                                   s_msg=f"Verified that attribute '{attribute}' of element located by '{locator}' ends with {exp_value}. Actual: {act}")

    def attribute_value_should_start_with(self, locator: str, attribute: str, exp_value: str):
        """Verify that the attribute of the element starts with the exp value, raises AssertionError if not."""
        act = self.get_attribute(locator=locator, attribute=attribute)
        assert_that_text_starts_with(act, exp_value,
                                     f"Expecting value of '{attribute}' attribute of element located by '{locator}' to start with {exp_value} but got {act}.",
                                     s_msg=f"Verified that attribute '{attribute}' of element located by '{locator}' start with {exp_value}. Actual: {act}.")

    def attribute_value_should_contain(self, locator: str, attribute: str, exp_value: str):
        """Verify that the attribute of the element contains the exp value, raises AssertionError if not."""
        act = self.get_attribute(locator=locator, attribute=attribute)
        assert_that_text_contains(act, exp_value,
                                  f"Expecting value of '{attribute}' attribute of element located by '{locator}' to contain {exp_value} but got {act}.",
                                  s_msg=f"Verified that attribute '{attribute}' of element located by '{locator}' contains {exp_value}. Actual: {act}.")

    def capture_page_screenshot(self, override_screenshot_setting: bool = False):
        """Capture page screenshot and embed it to the logs."""
        screenshot = override_screenshot_setting if override_screenshot_setting else self.__screenshot

        if screenshot:
            self.__ctx.capture_page_screenshot(filename="EMBED")

    def click(self, locator: str):
        """Click the element."""
        try:
            self.__exception_handler(func=self.highlight, locator=locator)
            self.__exception_handler(func=self.__ctx.click_element, locator=locator)
        except ElementClickInterceptedException or Exception:
            return self.__force_click_element_via_js_executor(locator=locator)

    def close_browser(self):
        """Close browser."""
        self.__ctx.close_browser()

    def close_all_browsers(self):
        """Close all browsers."""
        self.__ctx.close_all_browsers()

    def count(self, locator: str) -> int:
        """Returns the count of the elements."""
        return len(self.__exception_handler(func=self.__ctx.find_elements, locator=locator))

    def count_of_should_be(self, locator: str, exp_count: str):
        act_count = self.count(locator=locator)
        assert_equal(actual=act_count, exp=int(exp_count),
                     msg=f"Expecting count of element located by '{locator}' to be {exp_count} but got {act_count}.",
                     s_msg=f"Verified that count of element located by '{locator}' is {exp_count}. Actual: {act_count}.")

    def delete_text_via_keys(self, locator: str):
        """Delete texts using Ctrl + A  Delete ."""
        logger.info(f"Deleting text of element located by '{locator}' via keys")
        self.__exception_handler(func=self.highlight, locator=locator)
        element: WebElement = self.__exception_handler(func=self.__ctx.find_element, locator=locator)
        element.send_keys(Keys.CONTROL + "A")
        element.send_keys(Keys.DELETE)

    def deselect_all(self, locator: str):
        """Deselect all selected <select> options."""
        logger.info(f"Unselecting all options on the <select> element located by '{locator}'")
        self.__get_select_element(locator=locator).deselect_all()

    def deselect_by_value(self, locator: str, value: str):
        """Deselect selected <select> option by value."""
        logger.info(f"Unselecting option with value: {value} on the <select> element located by '{locator}'")
        self.__get_select_element(locator=locator).deselect_by_value(value=value)

    def deselect_by_index(self, locator: str, index: str):
        """Deselect selected <select> option by index."""
        logger.info(f"Unselecting option with index: {index} on the <select> element located by '{locator}'")
        self.__get_select_element(locator=locator).deselect_by_index(index=index)

    def double_click(self, locator: str):
        self.__exception_handler(func=self.__ctx.double_click_element, locator=locator)

    def find_elements(self, locator: str):
        return self.__ctx.find_elements(locator)

    def deselect_by_label(self, locator: str, label: str):
        """Deselect selected <select> option by label/visible text."""
        logger.info(f"Unselecting option with label: {label} on the <select> element located by '{locator}'")
        self.__get_select_element(locator=locator).deselect_by_visible_text(text=label)

    def get_attribute(self, locator: str, attribute: str) -> str:
        """Returns the attribute value of the element."""
        self.highlight(locator=locator)
        return self.__exception_handler(func=self.__ctx.get_element_attribute, locator=locator, attribute=attribute)

    def get_first_selected_option(self, locator: str) -> str:
        """Returns the first selected options of a <select> element."""
        return self.__get_select_element(locator=locator).first_selected_option.get_attribute("value")

    def get_text(self, locator: str) -> str:
        """Returns the text of the element. When using this, make sure that the locator is unique."""
        self.scroll_into_view(locator=locator)
        self.__exception_handler(func=self.highlight, locator=locator)
        return self.__exception_handler(func=self.__ctx.get_text, locator=locator)

    def get_texts(self, locator: str) -> list[str]:
        """Returns a list of texts of the element/s."""
        elements = self.__ctx.find_elements(locator=locator)
        return [self.__exception_handler(func=self.__ctx.get_text, locator=element) for element in elements]

    def get_value(self, locator: str) -> str:
        """Returns the value of the element. When using this, make sure that the locator is unique."""
        self.__exception_handler(func=self.highlight, locator=locator)
        return self.__exception_handler(func=self.__ctx.get_value, locator=locator)

    def get_values(self, locator: str):
        """Returns a list of values of the element/s."""
        elements = self.__ctx.find_elements(locator=locator)
        return [self.__exception_handler(func=self.__ctx.get_value, locator=element) for element in elements]

    def go_to(self, url: str):
        """Open the url on the current browser window."""
        self.__ctx.go_to(url=url)

    def highlight(self, locator: str):
        pass
        # try:
        #     self.__ctx.execute_javascript("arguments[0].setAttribute('style', 'border: 2px solid red;');", "ARGUMENTS",
        #                                   self.__ctx.find_element(locator=locator))
        # except TimeoutException:
        #     logger.debug(f"Selenium Timeout: {self.__ctx.get_selenium_timeout()}")
        #     logger.debug(traceback.format_exc())

    def input_text(self, locator: str, text: str, click: bool = True, press_enter: bool = False, clear: bool = True):
        """Input text to the element."""
        if click:
            self.click(locator=locator)

        self.__exception_handler(func=self.__ctx.input_text, locator=locator, text=text, clear=clear)

        if press_enter:
            self.press_enter(locator=locator)

    def input_password(self, locator: str, password: str, click: bool = True, press_enter: bool = False,
                       clear: bool = True):
        """Input password to the element."""
        if click:
            self.click(locator=locator)

        self.__exception_handler(func=self.__ctx.input_password, locator=locator, password=password, clear=clear)

        if press_enter:
            self.press_enter(locator=locator)

    def is_text(self, locator: str, exp_text: str, ignore_case: bool = False, ignore_space: bool = False,
                timeout: timedelta = None) -> bool:
        """Returns True if the element text matches the exp text, otherwise False."""
        if timeout:
            try:
                self.wait_until_text_is(locator=locator, exp_text=exp_text)
            except TimeoutException:
                pass

        act_text = self.get_text(locator=locator)
        exp_text_transformed = _transform(exp_text, ignore_case, ignore_space)
        act_text_transformed = _transform(act_text, ignore_case, ignore_space)
        return exp_text_transformed == act_text_transformed

    def is_text_a_valid_select_option(self, locator: str, text: str) -> bool:
        """Returns True if text is a valid <select> option, otherwise False."""
        return text in self.__get_all_select_options_text(locator=locator)

    def is_value_a_valid_select_option(self, locator: str, value: str) -> bool:
        """Returns True if value is a valid <select> option, otherwise False."""
        return value in self.__get_all_select_options_values(locator=locator)

    def is_value(self, locator: str, exp_value: str, ignore_case: bool = False, ignore_space: bool = False) -> bool:
        """Returns True if the element value matches the exp value, otherwise False."""
        act_value = self.get_value(locator=locator)
        exp_value_transformed = _transform(exp_value, ignore_case, ignore_space)
        act_value_transformed = _transform(act_value, ignore_case, ignore_space)
        return exp_value_transformed == act_value_transformed

    def is_visible(self, locator: str, timeout: timedelta = None) -> bool:
        """Returns True if the element is visible, otherwise False."""
        if timeout is None:
            timeout = self.__timeout
        try:
            self.wait_until_visible(locator=locator, timeout=timeout)
            return True
        except Exception:
            return False

    def is_enabled(self, locator: str, timeout: timedelta = None) -> bool:
        """Returns True if the element is enabled, otherwise False."""
        if timeout is None:
            timeout = self.__timeout
        try:
            self.wait_until_enabled(locator=locator, timeout=timeout)
            return True
        except Exception:
            return False

    def is_selected(self, locator: str):
        """Returns True if the element is selected, otherwise False."""
        return self.__exception_handler(func=self.__ctx.find_element, locator=locator).is_selected()

    def open_browser(self, url, browser, options, alias):
        """Creates a new web driver and then open the url on the specified browser."""
        self.__ctx.open_browser(url=url, browser=browser, options=options, alias=alias)

    def press_enter(self, locator: str):
        """Press enter."""
        logger.info(f"Press enter on element located by '{locator}'.")
        element: WebElement = self.__exception_handler(func=self.__ctx.find_element, locator=locator)
        element.send_keys(Keys.ENTER)

    def reload_browser(self):
        """Reload the browser."""
        self.__ctx.reload_page()

    def scroll_into_view(self, locator):
        """Scroll the element into view."""
        logger.info(f"Scroll element located by '{locator}' into view.")
        # self.__exception_handler(func=self.__ctx.scroll_element_into_view, locator=locator)
        try:
            self.__ctx.execute_javascript("arguments[0].scrollIntoView(true);", "ARGUMENTS",
                                          self.__ctx.find_element(locator=locator))
        except TimeoutException:
            logger.debug(f"Selenium Timeout: {self.__ctx.get_selenium_timeout()}")
            logger.debug(traceback.format_exc())

    def select_frame(self, locator: str):
        """Select the frame/iFrame."""
        self.__exception_handler(func=self.__ctx.select_frame, locator=locator)

    def select_options_should_contain_text(self, locator: str, exp_text: str):
        """Verify that the options of the <select> element contains the exp text, raise AssertionError if not."""
        options = self.__get_all_select_options_text(locator=locator)
        assert_that_list_contains_all(options, list(exp_text),
                                      f"Expecting options of select element located by '{locator}' to contain {exp_text} but is not in the available options.",
                                      s_msg=f"Verified that options of select element located by '{locator}' contains {exp_text}.")

    def select_options_should_contain_value(self, locator: str, exp_value: str):
        """Verify that the options of the <select> element contains the exp value, raise AssertionError if not."""
        options = self.__get_all_select_options_values(locator=locator)
        assert_that_list_contains_all(options, list(exp_value),
                                      f"Expecting options of select element located by '{locator}' to contain {exp_value} but is not in the available options.",
                                      s_msg=f"Verified that options of select element located by '{locator}' contains {exp_value}.")

    def switch_to_default_content(self):
        """Switch to default content."""
        self.__ctx.driver.switch_to.default_content()

    def should_be_visible(self, locator: str, timeout: timedelta = None):
        """Verify that the element is visible, raises AssertionError if not."""
        is_visible = self.is_visible(locator=locator, timeout=timeout)
        assert_true(expr=is_visible, msg=f"Expecting element located by '{locator}' to be visible but is not.",
                    s_msg=f"Verified that element located by '{locator}' is visible.")

    def should_not_be_visible(self, locator: str, timeout: timedelta = None):
        """Verify that the element is NOT visible, raises AssertionError if not."""
        is_visible = self.is_visible(locator=locator, timeout=timeout)
        assert_false(expr=is_visible, msg=f"Expecting element located by '{locator}' to NOT be visible but it is.",
                     s_msg=f"Verified that element located by '{locator}' is NOT visible.")

    def should_be_enabled(self, locator: str, timeout: timedelta = timedelta(seconds=0.5)):
        """Verify that the element is enabled, raises AssertionError if not."""
        is_enabled = self.is_enabled(locator=locator, timeout=timeout)
        assert_true(expr=is_enabled, msg=f"Expecting element located by '{locator}' to be enabled but is not.",
                    s_msg=f"Verified that element located by '{locator}' is enabled.")

    def should_be_selected(self, locator: str):
        """Verify that the element is selected,raises AssertionError if not.
        Applicable to checkbox / radio buttons. Uses selenium element.isSelected()
        """
        assert_true(self.is_selected(locator=locator),
                    msg=f"Expecting element located by '{locator}' to be selected but is not.",
                    s_msg=f"Verified that element located by '{locator}' is selected.")

    def should_not_be_selected(self, locator: str):
        """Verify that the element is not selected,raises AssertionError if it is selected.
            Applicable to checkbox / radio buttons. Uses selenium element.isSelected()
        """
        assert_false(self.is_selected(locator=locator),
                     msg=f"Expecting element located by '{locator}' to be NOT selected but it is.",
                     s_msg=f"Verified that element located by '{locator}' is NOT selected.")

    def should_be_disabled(self, locator: str, timeout: timedelta = timedelta(seconds=0.5)):
        """Verify that the element is disabled, raises AssertionError if not."""
        is_enabled = self.is_enabled(locator=locator, timeout=timeout)
        assert_false(expr=is_enabled, msg=f"Expecting element located by '{locator}' to be disabled but is not.",
                     s_msg=f"Verified that element located by '{locator}' is disabled.")

    def select_by_label(self, locator: str, label: str):
        """Select <select> element option by label/visible text."""
        logger.info(f"Selecting option with label: {label} on the <select> element located by '{locator}'")
        self.__get_select_element(locator=locator).select_by_visible_text(text=label)

    def select_by_random_value(self, locator: str):
        """Select random <select> element option by value except for the currently selected option. Returns the value of the selected option."""
        current = self.get_first_selected_option(locator=locator)
        options_by_value = self.__get_all_select_options_values(locator=locator)
        new = _random_item(options_by_value, except_for=current)
        self.select_by_value(locator=locator, value=new)
        return new

    def select_by_value(self, locator: str, value: str):
        """Select <select> element option by value."""
        logger.info(f"Selecting option with value: {value} on the <select> element located by '{locator}'")
        self.__get_select_element(locator=locator).select_by_value(value=value)

    def select_by_index(self, locator: str, index: str):
        """Select <select> element option by index."""
        logger.info(f"Selecting option with index: {index} on the <select> element located by '{locator}'")
        self.__get_select_element(locator=locator).select_by_index(index=index)

    def select_option_with_text_should_be_selected(self, locator: str, text: str):
        """Verify the <select> option with the specified text is selected, raises AssertionError if not."""
        selected_options = self.__get_selected_select_option_text(locator=locator)
        assert_that_list_has_item(selected_options, text,
                                  f"Expecting option {text} of select element located by '{locator}' to be selected but is not. Selected options are: {selected_options}.",
                                  f"Verified that option {text} of select element located by '{locator}' is selected.")

    def select_option_with_value_should_be_selected(self, locator: str, value: str):
        """Verify the <select> option with the specified value is selected, raises AssertionError if not."""
        selected_options = self.__get_selected_select_option_value(locator=locator)
        assert_that_list_has_item(selected_options, value,
                                  f"Expecting option {value} of select element located by '{locator}' to be selected but is not. Selected options are: {selected_options}.",
                                  f"Verified that option {value} of select element located by '{locator}' is selected.")

    def text_should_be(self, locator: str, exp_text: str, ignore_case: bool = False, ignore_space: bool = False,
                       with_wait: bool = False, strip: bool = False):
        """Verify that the element text matches the exp text, raise AssertionError if not."""

        if with_wait:
            try:
                act_text = self.wait_until_text_is(locator=locator, exp_text=exp_text)
            except TimeoutException:
                act_text = self.get_text(locator=locator)
        else:
            act_text = self.get_text(locator=locator)
        exp_text_transformed = _transform(exp_text, ignore_case, ignore_space, strip)
        act_text_transformed = _transform(act_text, ignore_case, ignore_space, strip)

        assert_equal(act_text_transformed, exp_text_transformed,
                     f"Expecting text of element located by '{locator}' to be {exp_text} but got {act_text}.",
                     f"Verified that the text of element located by '{locator}' is {exp_text}. Actual: {act_text}.")

    def text_should_be_empty(self, locator: str):
        """Verify that the element text is empty, raise AssertionError if not."""
        act_text = self.get_text(locator=locator)
        assert_equal(act_text, "",
                     msg=f"Expecting text of element located by '{locator}' to be empty but got {act_text}.",
                     s_msg=f"Verified that the text of element located by '{locator}' is empty.")

    def text_should_contain(self, locator: str, exp_text, ignore_case: bool = False, ignore_space: bool = False):
        """Verify that the element text contains the exp text, raise AssertionError if not."""
        act_text = self.get_text(locator=locator)
        exp_text_transformed = _transform(exp_text, ignore_case, ignore_space)
        act_text_transformed = _transform(act_text, ignore_case, ignore_space)

        assert_that_text_contains(act_text_transformed, exp_text_transformed,
                                  f"Expecting element located by '{locator}' to contain {exp_text} but got {act_text}",
                                  s_msg=f"Verified that the text of element located by '{locator}' contains {exp_text}. Actual: {act_text}.")

    def text_should_start_with(self, locator: str, exp_text: str, ignore_case: bool = False,
                               ignore_space: bool = False):
        """Verify that the element text starts with the exp text, raise AssertionError if not."""
        act_text = self.get_text(locator=locator)
        exp_text_transformed = _transform(exp_text, ignore_case, ignore_space)
        act_text_transformed = _transform(act_text, ignore_case, ignore_space)

        assert_that_text_starts_with(act_text_transformed, exp_text_transformed,
                                     f"Expecting text of element located by '{locator}' to start with {exp_text} but got {act_text}.",
                                     s_msg=f"Verified that the text of element located by '{locator}' starts with {exp_text}. Actual: {act_text}.")

    def text_should_end_with(self, locator: str, exp_text: str, ignore_case: bool = False, ignore_space: bool = False):
        """Verify that the element text ends with the exp text, raise AssertionError if not."""
        act_text = self.get_text(locator=locator)
        exp_text_transformed = _transform(exp_text, ignore_case, ignore_space)
        act_text_transformed = _transform(act_text, ignore_case, ignore_space)

        assert_that_text_ends_with(act_text_transformed, exp_text_transformed,
                                   f"Expecting text of element located by '{locator}' to end with {exp_text} but got {act_text}.",
                                   s_msg=f"Verified that the text of element located by '{locator}' ends with {exp_text}. Actual: {act_text}.")

    def text_should_not_be_empty(self, locator: str):
        """"Verify that the element text is not empty, raise AssertionError if not."""
        act_text = self.get_text(locator=locator)
        assert_that_text_is_not_empty(txt=act_text,
                                      msg=f"Expecting text of element located by {locator} to not be empty but is empty.",
                                      s_msg=f"Verified that the text of element located by '{locator}' is NOT empty. Actual: {act_text}.")

    def texts_should_contain(self, locator: str, exp_text: str):
        """Verify that the text of at least one of the elements located by the locator to be the exp text, raise AssertionError if not."""
        texts = self.get_texts(locator=locator)
        assert_true(exp_text in texts,
                    msg=f"Expecting that at least one of the element located by '{locator}' to have a text of {exp_text} but got {texts}.",
                    s_msg=f"Verified that the text of at least one of the elements located by '{locator}' is {exp_text}. Actual: {texts}.")

    def type_number(self, locator: str, number: str):
        """Type the number to the element via keys. Period (.) is in accepted for decimal points."""
        logger.info(f"Type number: {number} into element located by '{locator}'")
        element: WebElement = self.__exception_handler(func=self.__ctx.find_element, locator=locator)
        for char in number:
            self.__exception_handler(func=_click_number, el=element, number=char)

    def unselect_frame(self):
        """Unselect the current selected frame/iFrame."""
        logger.info("Unselecting Frame")
        self.__ctx.unselect_frame()

    def value_should_be(self, locator: str, exp_value: str, ignore_case: bool = False, ignore_space: bool = False):
        """Verify that the element value is the exp value, raise AssertionError if not."""
        act_value = self.get_value(locator=locator)
        act_value_transformed = _transform(text=act_value, remove_case=ignore_case, remove_spaces=ignore_space)
        exp_value_transformed = _transform(text=exp_value, remove_case=ignore_case, remove_spaces=ignore_space)

        assert_equal(act_value_transformed, exp_value_transformed,
                     f"Expecting value of element located by '{locator}' to be {exp_value} but got {act_value}.",
                     s_msg=f"Verified that the value of element located by '{locator}' is {exp_value}. Actual: {act_value}.")

    def value_should_be_empty(self, locator: str):
        """Verify that the element value is empty, raise AssertionError if not."""
        act_value = self.get_value(locator=locator)
        assert_equal(act_value, "",
                     msg=f"Expecting value of element located by '{locator}' to be empty but got {act_value}.",
                     s_msg=f"Verified that the value of element located by '{locator}' is EMPTY.")

    def value_should_not_be_empty(self, locator: str):
        """Verify that the element value is not empty, raise AssertionError if not."""
        act_value = self.get_value(locator=locator)
        assert_that_text_is_not_empty(txt=act_value,
                                      msg=f"Expecting value of element located by {locator} to not be empty but is empty.",
                                      s_msg=f"Verified that the value of element located by '{locator}' is NOT EMPTY.")

    def value_should_contain(self, locator: str, exp_text, ignore_case: bool = False, ignore_space: bool = False):
        """Verify that the element value contains, raise AssertionError if not."""
        act_value = self.get_value(locator=locator)
        act_value_transformed = _transform(text=act_value, remove_case=ignore_case, remove_spaces=ignore_space)
        exp_text_transformed = _transform(text=exp_text, remove_case=ignore_case, remove_spaces=ignore_space)

        assert_that_text_contains(txt=act_value_transformed, content=exp_text_transformed,
                                  msg=f"Expecting value of element located by '{locator}' to contain {exp_text} but got {act_value}.",
                                  s_msg=f"Verified that the value of element located by '{locator}' contains {exp_text}. Actual: {act_value}.")

    def value_should_start_with(self, locator: str, exp_text, ignore_case: bool = False, ignore_space: bool = False):
        """Verify that the element value starts with the exp value, raise AssertionError if not."""
        act_value = self.get_value(locator=locator)
        act_value_transformed = _transform(text=act_value, remove_case=ignore_case, remove_spaces=ignore_space)
        exp_text_transformed = _transform(text=exp_text, remove_case=ignore_case, remove_spaces=ignore_space)

        assert_that_text_starts_with(txt=act_value_transformed, start=exp_text_transformed,
                                     msg=f"Expecting value of element located by '{locator}' to start with {exp_text} but got {act_value}.",
                                     s_msg=f"Verified that the value of element located by '{locator}' starts with {exp_text}. Actual: {act_value}.")

    def value_should_end_with(self, locator: str, exp_text, ignore_case: bool = False, ignore_space: bool = False):
        """Verify that the element value ends with the exp value, raise AssertionError if not."""
        act_value = self.get_value(locator=locator)
        act_value_transformed = _transform(text=act_value, remove_case=ignore_case, remove_spaces=ignore_space)
        exp_text_transformed = _transform(text=exp_text, remove_case=ignore_case, remove_spaces=ignore_space)

        assert_that_text_ends_with(txt=act_value_transformed, end=exp_text_transformed,
                                   msg=f"Expecting value of element located by '{locator}' to end with {exp_text} but got {act_value}.",
                                   s_msg=f"Verified that the value of element located by '{locator}' end with {exp_text}. Actual: {act_value}.")

    def wait_until_attribute_value_contains(self, locator: str, attribute: str, exp_value: str,
                                            timeout: timedelta = None) -> str:
        """Wait until the element attribute contains the exp attribute.
        Return the actual value if present,raises TimeoutException otherwise.
        """
        logger.info(
            f"Wait until value of {attribute} attribute of element located by '{locator}' to contain {exp_value}.")
        if timeout is None:
            timeout = self.__timeout

        retries = _get_retry_count(timeout=timeout)
        delay = timeout.total_seconds() / retries
        act_value = self.get_attribute(locator=locator, attribute=attribute)
        present = False

        while not present:
            if retries == 0:
                break
            if exp_value in act_value:
                present = True
                break
            sleep(seconds=delay)
            act_value = self.get_attribute(locator=locator, attribute=attribute)
            retries -= 1

        if not present:
            raise TimeoutException(
                f"Cannot wait until '{attribute}' attribute of element located by '{locator}' to contain {exp_value}. Actual attribute: {act_value}.")

        return act_value

    def wait_until_count_is_greater_than(self, locator: str, count: int, timeout: timedelta = None) -> int:
        """Wait until the element count is greater than the exp count.
         Return the actual count if greater than the exp count,raises TimeoutException otherwise.
         """
        logger.info(f"Wait until count of elements located by '{locator}' to be greater than {count}.")
        if timeout is None:
            timeout = self.__timeout

        retries = _get_retry_count(timeout=timeout)
        delay = timeout.total_seconds() / retries
        act_count = self.count(locator=locator)
        while act_count <= count:
            if retries == 0:
                break

            sleep(seconds=delay)
            act_count = self.count(locator=locator)
            retries -= 1

        if act_count <= count:
            raise TimeoutException(
                f"Cannot wait until count of element located by '{locator}' to be greater than {count}. Actual count: {act_count}.")

        return act_count

    def wait_until_text_is(self, locator: str, exp_text: str, ignore_case: bool = False, ignore_space: bool = False,
                           timeout: timedelta = None) -> str:
        """Wait until the element text is the exp text.
         Return the actual text if present,raises TimeoutException otherwise.
         """
        logger.info(f"Wait until text of element located by '{locator}' to be {exp_text}.")
        if timeout is None:
            timeout = self.__timeout

        retries = _get_retry_count(timeout=timeout)
        delay = timeout.total_seconds() / retries

        exp_text_transformed = _transform(exp_text, ignore_case, ignore_space)

        act_text = self.get_text(locator=locator)
        act_text_transformed = _transform(act_text, ignore_case, ignore_space)

        while exp_text_transformed != act_text_transformed:
            if retries == 0:
                break
            sleep(seconds=delay)
            act_text = self.get_text(locator=locator)
            act_text_transformed = _transform(act_text, ignore_case, ignore_space)
            retries -= 1

        if exp_text_transformed != act_text_transformed:
            raise TimeoutException(
                f"Cannot for the text of element located by '{locator}' to be {exp_text}. Actual text: {act_text}")

        return act_text

    def wait_until_text_is_not_empty(self, locator: str, timeout: timedelta = None) -> str:
        """Wait until the element text is not empty.
         Return the actual text if present,raises TimeoutException otherwise.
         """
        logger.info(f"Wait until text of element located by '{locator}' is not empty.")
        if timeout is None:
            timeout = self.__timeout

        retries = _get_retry_count(timeout=timeout)
        delay = timeout.total_seconds() / retries
        text = self.get_text(locator=locator)

        while (text is None) or (len(text) == 0):
            if retries == 0:
                break
            sleep(delay)
            text = self.get_text(locator=locator)
            retries -= 1

        if (text is None) or (len(text) == 0):
            raise Exception(f"Can't wait for the text of element located by '{locator}' to appear.")

        return text

    def wait_until_found(self, locator: str, timeout: timedelta = None):
        """Wait until element is found."""
        self.__wait_until_element_is_found(locator=locator, timeout=timeout)

    def wait_until_value_is_not_empty(self, locator: str, timeout: timedelta = None) -> str:
        """Wait until the element value is not empty.
           Return the actual value if present,raises TimeoutException otherwise.
           """
        logger.info(f"Wait until value of element located by '{locator}' is not empty.")
        if timeout is None:
            timeout = self.__timeout

        retries = _get_retry_count(timeout=timeout)
        delay = timeout.total_seconds() / retries
        value = self.get_value(locator=locator)
        while (value is None) or (len(value) == 0):
            if retries == 0:
                break
            sleep(delay)
            value = self.get_value(locator=locator)
            retries -= 1

        if (value is None) or (len(value) == 0):
            raise Exception(f"Can't for the value of element located by '{locator}' to appear.")

        return value

    def wait_until_value_is(self, locator: str, exp_value: str, ignore_case: bool = False, ignore_space: bool = False,
                            timeout: timedelta = None) -> str:
        """Wait until the element value is the exp value.
            Return the actual value if present,raises TimeoutException otherwise.
            """
        logger.info(f"Wait until value of element located by '{locator}' is {exp_value}.")
        if timeout is None:
            timeout = self.__timeout

        retries = _get_retry_count(timeout=timeout)
        delay = timeout.total_seconds() / retries

        exp_value_transformed = _transform(exp_value, ignore_case, ignore_space)

        act_value = self.get_value(locator=locator)
        act_value_transformed = _transform(act_value, ignore_case, ignore_space)

        while exp_value_transformed != act_value_transformed:
            if retries == 0:
                break
            sleep(seconds=delay)
            act_value = self.get_value(locator=locator)
            act_value_transformed = _transform(act_value, ignore_case, ignore_space)
            retries -= 1

        if exp_value_transformed != act_value_transformed:
            raise TimeoutException(
                f"Cannot wait for the value of element located by '{locator}' to be {exp_value}. Actual value: {act_value}.")

        return act_value

    def wait_until_visible(self, locator: str, timeout: timedelta = None):
        """Waits until element is visible."""
        logger.info(f"Wait until element located by '{locator}' is visible.")
        if timeout is None:
            timeout = self.__timeout
        self.__exception_handler(func=self.__ctx.wait_until_element_is_visible, locator=locator, timeout=timeout)

    def wait_until_interactible(self, locator: str, timeout: timedelta = None):
        """Wait until element is interactible."""
        logger.info(f"Wait until element located by '{locator}' is interactible.")
        if timeout is None:
            timeout = self.__timeout
        self.__exception_handler(func=self.__wait_until_element_is_interactible, locator=locator, timeout=timeout)

    def wait_until_not_visible(self, locator: str, timeout: timedelta = None):
        """Wait until element is not visible."""
        logger.info(f"Wait until element located by '{locator}' is not visible.")
        if timeout is None:
            timeout = self.__timeout
        self.__exception_handler(func=self.__ctx.wait_until_element_is_not_visible, locator=locator, timeout=timeout)

    def wait_until_enabled(self, locator: str, timeout: timedelta = None):
        """Waits until element is enabled."""
        logger.info(f"Wait until element located by '{locator}' is enabled.")
        if timeout is None:
            timeout = self.__timeout
        self.__exception_handler(func=self.__ctx.wait_until_element_is_enabled, locator=locator, timeout=timeout)

    def __get_select_element(self, locator: str) -> Select:
        self.__exception_handler(func=self.highlight, locator=locator)
        element = self.__exception_handler(func=self.__ctx.find_element, locator=locator)
        return Select(webelement=element)

    def __exception_handler(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ElementNotFound:
            self.__wait_until_element_is_found(locator=kwargs.get("locator"), timeout=kwargs.get("timeout"))
            return func(*args, **kwargs)
        except ElementNotInteractableException:
            self.__wait_until_element_is_interactible(locator=kwargs.get("locator"), timeout=kwargs.get("timeout"))
            return func(*args, **kwargs)
        except StaleElementReferenceException:
            self.__wait_until_element_is_not_stale(locator=kwargs.get("locator"), timeout=kwargs.get("timeout"))
            return func(*args, **kwargs)

    def __wait_until_element_is_found(self, locator: str, timeout: timedelta = None):
        if timeout is None:
            timeout = self.__timeout

        retries = _get_retry_count(timeout=timeout)
        delay = timeout.total_seconds() / retries
        elements = self.__ctx.find_elements(locator=locator)

        while len(elements) == 0:
            sleep(delay)
            elements = self.__ctx.find_elements(locator=locator)

            if retries == 0:
                break
            retries -= 1

        if len(elements) == 0:
            raise ElementNotFound(f"Element with locator '{locator}' not found.")

    def __wait_until_element_is_interactible(self, locator: str, timeout: timedelta = None):
        if timeout is None:
            timeout = self.__timeout

        retries = _get_retry_count(timeout=timeout)
        delay = timeout.total_seconds() / retries
        interactible = False

        while retries > 0:
            try:
                self.__ctx.get_text(locator=locator)
                self.__ctx.get_value(locator=locator)
                interactible = True
                break
            except ElementNotInteractableException:
                sleep(delay)
            except ElementClickInterceptedException:
                sleep(delay)
            retries -= 1

        if not interactible:
            raise ElementNotInteractableException(f"Element located by '{locator}' is not interactible.")

    def __wait_until_element_is_not_stale(self, locator: str, timeout: timedelta = None):
        if timeout is None:
            timeout = self.__timeout

        retries = _get_retry_count(timeout=timeout)
        delay = timeout.total_seconds() / retries
        stale = True

        while retries > 0:
            try:
                self.__ctx.get_text(locator)
                self.__ctx.get_value(locator)
                stale = False
                break
            except StaleElementReferenceException:
                sleep(delay)
            retries -= 1

        if stale:
            raise StaleElementReferenceException(f"Element located by '{locator}' is stale.")

    def __force_click_element_via_js_executor(self, locator: str):
        try:
            self.__ctx.execute_javascript("arguments[0].click()", "ARGUMENTS", self.__ctx.find_element(locator=locator))
        except TimeoutException:
            logger.debug(f"Selenium Timeout: {self.__ctx.get_selenium_timeout()}")
            logger.debug(traceback.format_exc())

    def __get_all_select_options_text(self, locator: str) -> list[str]:
        """Returns a list of the options visible text."""
        return [el.text for el in self.__get_select_element(locator=locator).options]

    def __get_selected_select_option_text(self, locator: str) -> list[str]:
        return [el.text for el in self.__get_select_element(locator=locator).all_selected_options]

    def __get_all_select_options_values(self, locator: str) -> list[str]:
        """Returns a list of the options values."""
        return [el.get_attribute("value") for el in self.__get_select_element(locator=locator).options]

    def __get_selected_select_option_value(self, locator: str) -> list[str]:
        return [el.get_attribute("value") for el in self.__get_select_element(locator=locator).all_selected_options]
