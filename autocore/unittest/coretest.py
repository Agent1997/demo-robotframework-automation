import unittest

from SeleniumLibrary import SeleniumLibrary

from autocore.web.core import Element

SAUCE_LABS_URL = "https://www.saucedemo.com/"
SL_USERNAME_LOC = "id:user-name"
SL_SUBMIT_BTN = "id:login-button"
SL_ERROR_DISPLAY = "xpath://h3[@data-test='error']"
BROWSER = "chrome"


class CoreWebElementTests(unittest.TestCase):

    def setUp(self) -> None:
        self.se = SeleniumLibrary()

    def tearDown(self) -> None:
        self.se.close_browser()

    def test_attribute_contains_true(self):
        self.se.open_browser(url=SAUCE_LABS_URL, browser=BROWSER)
        username = Element(self.se, SL_USERNAME_LOC)
        result = username.attribute_contains("data-test", "name")
        self.assertTrue(result)

    def test_attribute_contains_true_2(self):
        self.se.open_browser(url=SAUCE_LABS_URL, browser=BROWSER)
        username = Element(self.se, SL_SUBMIT_BTN)
        result = username.attribute_contains("class", "btn_action")
        self.assertTrue(result)

    def test_attribute_contains_false(self):
        self.se.open_browser(url=SAUCE_LABS_URL, browser=BROWSER)
        username = Element(self.se, SL_USERNAME_LOC)
        result = username.attribute_contains("data-test", "names")
        self.assertFalse(result)

    def test_attribute_contains_false_2(self):
        self.se.open_browser(url=SAUCE_LABS_URL, browser=BROWSER)
        username = Element(self.se, SL_SUBMIT_BTN)
        result = username.attribute_contains("class", "login-button")
        self.assertFalse(result)

    def test_pass_attribute_value_should_be(self):
        self.se.open_browser(url=SAUCE_LABS_URL, browser=BROWSER)
        username = Element(self.se, SL_USERNAME_LOC)
        username.attribute_value_should_be("data-test", "username")

    def test_fail_attribute_value_should_be(self):
        self.se.open_browser(url=SAUCE_LABS_URL, browser=BROWSER)
        username = Element(self.se, SL_USERNAME_LOC)
        with self.assertRaises(AssertionError):
            username.attribute_value_should_be("data-test", "incorrectvalue")

    def test_click_and_get_text(self):
        self.se.open_browser(url=SAUCE_LABS_URL, browser=BROWSER)
        login = Element(self.se, SL_SUBMIT_BTN)
        error_display = Element(self.se, SL_ERROR_DISPLAY)
        login.click()
        result = error_display.get_text()
        self.assertEqual(result, "Epic sadface: Username is required")

    def test_pass_click_and_text_should_be(self):
        self.se.open_browser(url=SAUCE_LABS_URL, browser=BROWSER)
        login = Element(self.se, SL_SUBMIT_BTN)
        error_display = Element(self.se, SL_ERROR_DISPLAY)
        login.click()
        error_display.text_should_be("Epic sadface: Username is required")

    def test_fail_click_and_text_should_be(self):
        self.se.open_browser(url=SAUCE_LABS_URL, browser=BROWSER)
        login = Element(self.se, SL_SUBMIT_BTN)
        error_display = Element(self.se, SL_ERROR_DISPLAY)
        login.click()
        with self.assertRaises(AssertionError):
            error_display.text_should_be("Epic sadface: Username is requiredd")

    def test_input_text_and_value_should_be_and_delete_text_via_keys(self):
        self.se.open_browser(url=SAUCE_LABS_URL, browser=BROWSER)
        username = Element(self.se, SL_USERNAME_LOC)
        username.input_text("Test Username")
        username.value_should_be("Test Username")
        username.value_should_be("Test Username", ignore_space=True)
        username.value_should_be("Test Username", ignore_space=True, ignore_case=True)
        username.value_should_not_be_empty()
        username.value_should_contain("User")
        username.value_should_end_with("rname")
        username.value_should_start_with("Test")
        username.delete_text_via_keys()
        username.value_should_be("")

    def test_press_enter(self):
        self.se.open_browser(url=SAUCE_LABS_URL, browser=BROWSER)
        login = Element(self.se, SL_SUBMIT_BTN)
        error_display = Element(self.se, SL_ERROR_DISPLAY)
        login.press_enter()
        error_display.text_should_be("Epic sadface: Username is required")
        error_display.text_should_be("Epic sadface: Username is required", ignore_case=True)
        error_display.text_should_be("Epic sadface: Username is required", ignore_case=True, ignore_space=True)
        error_display.text_should_end_with("required")
        error_display.text_should_start_with("Epic")
        error_display.text_should_contain("Username")
        error_display.text_should_not_be_empty()

    def test_type_number_test(self):
        self.se.open_browser(url=SAUCE_LABS_URL, browser=BROWSER)
        username = Element(self.se, SL_USERNAME_LOC)
        username.value_should_be("")
        username.type_number("12354.525")
        username.value_should_be("12354.525")
        username.wait_until_value_is("12354.525")
        username.wait_until_value_is_not_empty()
        username.delete_text_via_keys()
        username.value_should_be("")

    def test_is_text_true(self):
        self.se.open_browser(url=SAUCE_LABS_URL, browser=BROWSER)
        login = Element(self.se, SL_SUBMIT_BTN)
        error_display = Element(self.se, SL_ERROR_DISPLAY)
        login.press_enter()
        res = error_display.is_text("Epic sadface: Username is required")
        self.assertTrue(res)

    def test_is_text_false(self):
        self.se.open_browser(url=SAUCE_LABS_URL, browser=BROWSER)
        login = Element(self.se, SL_SUBMIT_BTN)
        error_display = Element(self.se, SL_ERROR_DISPLAY)
        login.press_enter()
        res = error_display.is_text("Epic sadface: Username is requiredd")
        self.assertFalse(res)


if __name__ == "__main__":
    unittest.main()
