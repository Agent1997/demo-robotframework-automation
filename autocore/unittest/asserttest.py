import unittest

from ddt import ddt, data

from autocore import asserts
from autocore.asserts import SoftAssert, assert_that_date_format_is


@ddt
class AssertsTests(unittest.TestCase):
    robot_info_log_prefix = "INFO:RobotFramework:"

    @data("1", 1, 1.5, "hello world", [1, 2, 3], ["1", "2", "three"])
    def test_passed_assert_equal(self, test_data):
        exp_log = AssertsTests.robot_info_log_prefix + "Verified that: {0} is equal to {1}.".format(test_data,
                                                                                                    test_data)
        with self.assertLogs(level='INFO') as log:
            asserts.assert_equal(test_data, test_data)

        self.assertEqual([exp_log], log.output)

    @data((1, 2), ("One", "one"), (1.5, 1.6), ([1, 2], [2, 3]))
    def test_failed_assert_equal_without_msg(self, test_data):
        test_data1, test_data2 = test_data
        exp_err_msg = "{0} is not equal to {1}.".format(test_data1, test_data2)
        with self.assertRaises(AssertionError) as e:
            asserts.assert_equal(test_data1, test_data2)

        self.assertEqual(exp_err_msg, str(e.exception))

    @data((1, 2, "Error msg 1"), ("One", "one", "Error msg 2"), (1.5, 1.6, "Error msg 3"),
          ([1, 2], [2, 3], "Error msg 4"))
    def test_failed_assert_equal_with_message(self, test_data):
        test_data1, test_data2, exp_err_msg = test_data
        with self.assertRaises(AssertionError) as e:
            asserts.assert_equal(test_data1, test_data2, exp_err_msg)
        self.assertEqual(exp_err_msg, str(e.exception))

    def test_fail_without_msg(self):
        with self.assertRaises(AssertionError) as e:
            asserts.fail()
        self.assertEqual("Fail Test.", str(e.exception))

    def test_fail_with_msg(self):
        exp_msg = "Custome err msg"
        with self.assertRaises(AssertionError) as e:
            asserts.fail(exp_msg)
        self.assertEqual(exp_msg, str(e.exception))

    @data(1 == 1, None is None, 5 > 4, 4 < 10, True, "True", [1])
    def test_passed_assert_true(self, test_data):
        exp_log = AssertsTests.robot_info_log_prefix + "Verified that expression passed as 'expr' is True."
        with self.assertLogs(level='INFO') as log:
            asserts.assert_true(test_data)

        self.assertEqual([exp_log], log.output)

    @data(1 != 1, 5 is None, 5 == 4, 4 > 10, False, "", [])
    def test_failed_assert_true_without_passed_msg(self, test_data):
        exp_err_msg = "The expression passed as 'expr' is not True."
        with self.assertRaises(AssertionError) as e:
            asserts.assert_true(test_data)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data((1 != 1, "Error msg1"), (5 is None, "Error msg2"), (5 == 4, "Error Msg3"), (4 > 10, "cust err"),
          (False, "error mg"), ("", "Empty string"), ([], "ae"))
    def test_failed_assert_true_with_passed_msg(self, test_data):
        expr, exp_err_msg = test_data
        with self.assertRaises(AssertionError) as e:
            asserts.assert_true(expr, exp_err_msg)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data("ad".endswith("a"), 1 > 5, "", [], 0)
    def test_passed_assert_false(self, test_expr):
        exp_log = AssertsTests.robot_info_log_prefix + "Verified that the expression passed as 'expr' is False."

        with self.assertLogs(level='INFO') as log:
            asserts.assert_false(test_expr)

        self.assertEqual([exp_log], log.output)

    @data("test", 1, [1, 2], True, 1 > 0)
    def test_failed_assert_false_without_msg(self, test_expr):
        exp_err_msg = "The expression passed as 'expr' is not False."
        with self.assertRaises(AssertionError) as e:
            asserts.assert_false(test_expr)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data(("test", "Error msg"), (1, "cust err msg"), ([1, 2], "Error msg 3"), (True, "Error"), (1 > 0, "test error"))
    def test_failed_assert_false_with_msg(self, test_data):
        test_expr, exp_err_msg = test_data
        with self.assertRaises(AssertionError) as e:
            asserts.assert_false(test_expr, exp_err_msg)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data(("hello", "he"), ("world hello", "world"), ("you tube", "you t"))
    def test_passed_assert_that_text_starts_with(self, test_data):
        txt, start = test_data
        exp_log = AssertsTests.robot_info_log_prefix + "Verified that: {0} starts with {1}.".format(txt, start)
        with self.assertLogs(level="INFO") as log:
            asserts.assert_that_text_starts_with(txt, start)
        self.assertEqual([exp_log], log.output)

    @data(("hello", "el"), ("world hello", "hello"), ("you tube", "yube"))
    def test_failed_assert_that_text_starts_without_msg(self, test_data):
        txt, start = test_data
        exp_err_msg = "{0} does not start with {1}.".format(txt, start)
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_text_starts_with(txt, start)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data(("hello", "el", "errmsg"), ("world hello", "hello", "errmsg1"), ("you tube", "yube", "errmsg3"))
    def test_failed_assert_that_text_starts_with_msg(self, test_data):
        txt, start, exp_err_msg = test_data
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_text_starts_with(txt, start, exp_err_msg)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data(("Maria Clara", "ara"), ("Santa Maria", "Maria"), ("Bella Bells", "a Bells"))
    def test_passed_assert_that_text_ends_with(self, test_data):
        txt, end = test_data
        exp_log = AssertsTests.robot_info_log_prefix + "Verified that: {0} ends with {1}.".format(txt, end)
        with self.assertLogs(level="INFO") as log:
            asserts.assert_that_text_ends_with(txt, end)
        self.assertEqual([exp_log], log.output)

    @data(("Maria Clara", "cara"), ("Santa Maria", "S Maria"), ("Bella Bells", "Bells "))
    def test_failed_assert_that_text_ends_with_no_msg(self, test_data):
        txt, end = test_data
        exp_err_msg = "{0} does not end with {1}.".format(txt, end)
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_text_ends_with(txt, end)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data(("Maria Clara", "cara", "err1"), ("Santa Maria", "S Maria", "err2"), ("Bella Bells", "Bells ", "err3"))
    def test_failed_assert_that_text_ends_with_msg(self, test_data):
        txt, end, exp_err_msg = test_data
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_text_ends_with(txt, end, exp_err_msg)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data(("My String", "Str"), ("Hello World", "lo W"))
    def test_passed_assert_that_text_contains(self, test_data):
        txt, content = test_data
        exp_log = AssertsTests.robot_info_log_prefix + "Verified that: {0} contains {1}.".format(txt, content)
        with self.assertLogs(level="INFO") as log:
            asserts.assert_that_text_contains(txt, content)
        self.assertEqual([exp_log], log.output)

    @data(("My String", "Strs"), ("Hello World", "loW"))
    def test_failed_assert_that_text_contains_without_msg(self, test_data):
        txt, content = test_data
        exp_err_msg = "{0} does not contain {1}.".format(txt, content)
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_text_contains(txt, content)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data(("My String", "Strs", "err1"), ("Hello World", "loW", "err2"))
    def test_failed_assert_that_text_contains_without_msg(self, test_data):
        txt, content, exp_err_msg = test_data
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_text_contains(txt, content, exp_err_msg)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data("String1", "STring 2", "one two tree", " ")
    def test_passed_assert_that_text_is_not_empty(self, test_data):
        asserts.assert_that_text_is_not_empty(test_data)

    @data("", None)
    def test_failed_assert_that_text_is_not_empty_no_msg(self, test_data):
        exp_err_msg = "Provided text is empty."
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_text_is_not_empty(test_data)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data(("", "String is empty"), (None, "String is None"))
    def test_failed_assert_that_text_is_not_empty_with_message(self, test_data):
        value, exp_err_msg = test_data
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_text_is_not_empty(value, exp_err_msg)
        self.assertEqual(exp_err_msg, str(e.exception))

    def test_passed_assert_that_list_is_empty(self):
        lst = []
        exp_log = AssertsTests.robot_info_log_prefix + "Verified that: list {0} is empty.".format(lst)
        with self.assertLogs(level="INFO") as log:
            asserts.assert_that_list_is_empty(lst)
        self.assertEqual([exp_log], log.output)

    @data([1, 2, 3], ["1", "2", "3"])
    def test_failed_assert_that_list_is_empty_without_msg(self, test_data):
        exp_err_msg = "List {0} is not empty.".format(test_data)
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_list_is_empty(test_data)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data(([1, 2, 3], "err1"), (["1", "2", "3"], "err2"))
    def test_failed_assert_that_list_is_empty_with_msg(self, test_data):
        lst, exp_err_msg = test_data
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_list_is_empty(lst, exp_err_msg)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data([1, 2, 3], ["one", "two", "three"])
    def test_passed_assert_that_list_is_not_empty(self, lst):
        exp_log = AssertsTests.robot_info_log_prefix + "Verified that: list {0} is not empty.".format(lst)
        with self.assertLogs(level="INFO") as log:
            asserts.assert_that_list_is_not_empty(lst)
        self.assertEqual([exp_log], log.output)

    def test_failed_assert_list_list_not_empty_without_msg(self):
        lst = []
        exp_err_msg = "List {0} is empty.".format(lst)
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_list_is_not_empty(lst)
        self.assertEqual(exp_err_msg, str(e.exception))

    def test_failed_assert_list_list_not_empty_with_msg(self):
        lst = []
        exp_err_msg = "Custom message"
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_list_is_not_empty(lst, exp_err_msg)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data(([1, 2, 3, 4], 4), ([11, 11, 23, 45], 11), (["ONE", "one", 1], 1))
    def test_passed_assert_that_list_has_item(self, test_data):
        lst, content = test_data
        exp_log = AssertsTests.robot_info_log_prefix + "Verified that: list {0} contains {1}.".format(lst, content)
        with self.assertLogs(level="INFO") as log:
            asserts.assert_that_list_has_item(lst, content)
        self.assertEqual([exp_log], log.output)

    @data(([1, 2, 3, 4], 6), ([11, 11, 23, 45], 56), (["ONE", "one", 1], "tow"))
    def test_failed_assert_that_list_has_item_without_msg(self, test_data):
        lst, content = test_data
        exp_err_msg = "List {0} does not contain {1}.".format(lst, content)
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_list_has_item(lst, content)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data(([1, 2, 3, 4], 6, "err1 msg"), ([11, 11, 23, 45], 56, "err2 msg"), (["ONE", "one", 1], "tow", "err3 msg"))
    def test_failed_assert_that_list_has_item_with_msg(self, test_data):
        lst, content, exp_err_msg = test_data
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_list_has_item(lst, content, exp_err_msg)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data(([1, 2, 3, 4], 5), ([11, 11, 23, 45], 55), (["ONE", "one", 1], "two"))
    def test_passed_assert_that_list_does_not_contain(self, test_data):
        lst, content = test_data
        exp_log = AssertsTests.robot_info_log_prefix + f"Verified that list {lst} does not contain {content}."
        with self.assertLogs(level="INFO") as log:
            asserts.assert_that_list_does_not_contain(lst, content)
        self.assertEqual([exp_log], log.output)

    @data(([1, 2, 3, 4], 4), ([11, 11, 23, 45], 11), (["ONE", "one", 1], "one"))
    def test_failed_assert_that_list_does_not_contain(self, test_data):
        lst, content = test_data
        exp_err_msg = f"List {lst} contains {content}."
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_list_does_not_contain(lst, content)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data(([1, 2, 3, 4, 5, 6], [1, 3, 5, 6]), (["one", "two"], ["one", "two"]), ([1, 2, "three"], ["three"]),
          ([1, 2, 3], [2, 2]))
    def test_passed_assert_that_list_contains_all(self, test_data):
        lst, contents = test_data
        exp_log = AssertsTests.robot_info_log_prefix + "Verified that: list {0} contains all of {1}.".format(lst,
                                                                                                             contents)
        with self.assertLogs(level="INFO") as log:
            asserts.assert_that_list_contains_all(lst, contents)
        self.assertEqual([exp_log], log.output)

    @data(([1, 2, 3, 4, 5], [1, 2, 4, 6, 7], [6, 7]))
    def test_failed_assert_that_list_contains_all_without_msg(self, test_data):
        lst, contents, missing_items = test_data
        exp_err_msg = "List {0} does not contain all of {1}. See missing item/s: {2}.".format(lst, contents,
                                                                                              missing_items)
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_list_contains_all(lst, contents)
        self.assertEqual(exp_err_msg, str(e.exception))

    @data(([1, 2, 3, 4, 5], [1, 2, 4, 6, 7], [6, 7], "err msg"))
    def test_failed_assert_that_list_contains_all_with_msg(self, test_data):
        lst, contents, missing_items, exp_err_msg = test_data
        with self.assertRaises(AssertionError) as e:
            asserts.assert_that_list_contains_all(lst, contents, exp_err_msg)
        self.assertEqual(exp_err_msg, str(e.exception))

    def test_passed_soft_asserts(self):
        str1 = str2 = "string"
        start = "str"
        end = "ing"
        str_content = "trin"
        lst = [1, 2]
        assert_equal_log = f"{AssertsTests.robot_info_log_prefix}Verified that: {str1} is equal to {str2}."
        assert_true_log = f"{AssertsTests.robot_info_log_prefix}Verified that expression passed as 'expr' is True."
        assert_false_log = f"{AssertsTests.robot_info_log_prefix}Verified that the expression passed as 'expr' is False."
        assert_str_start_with_log = f"{AssertsTests.robot_info_log_prefix}Verified that: {str1} starts with {start}."
        assert_str_end_with_log = f"{AssertsTests.robot_info_log_prefix}Verified that: {str1} ends with {end}."
        assert_str_contains_log = f"{AssertsTests.robot_info_log_prefix}Verified that: {str1} contains {str_content}."
        assert_list_is_empty_log = f"{AssertsTests.robot_info_log_prefix}Verified that: list {[]} is empty."
        assert_list_is_not_empty_log = f"{AssertsTests.robot_info_log_prefix}Verified that: list {lst} is not empty."
        assert_list_contains_log = f"{AssertsTests.robot_info_log_prefix}Verified that: list {lst} contains {lst[0]}."
        assert_list_contains_all_log = f"{AssertsTests.robot_info_log_prefix}Verified that: list" \
                                       f" {lst} contains all of {lst}."
        with self.assertLogs(level="INFO") as log:
            sa = SoftAssert()
            sa.assert_equal(str1, str2)
            sa.assert_true(True)
            sa.assert_false(False)
            sa.assert_that_text_starts_with(str1, start)
            sa.assert_that_text_ends_with(str1, end)
            sa.assert_that_text_contains(str1, str_content)
            sa.assert_that_list_is_empty([])
            sa.assert_that_list_is_not_empty(lst)
            sa.assert_that_list_has_item(lst, lst[0])
            sa.assert_that_list_contains_all(lst, lst)
            sa.assert_all()

        self.assertEqual([
            assert_equal_log,
            assert_true_log,
            assert_false_log,
            assert_str_start_with_log,
            assert_str_end_with_log,
            assert_str_contains_log,
            assert_list_is_empty_log,
            assert_list_is_not_empty_log,
            assert_list_contains_log,
            assert_list_contains_all_log
        ], log.output)

    def test_failed_soft_assert(self):
        str1 = "String"
        str2 = "String 2"
        end = "str"
        content = "dobidubidu"
        custom_err_msg = "This is a custom error message."
        lst = [1, 24, 65]

        err_msgs = [
            f"{str1} is not equal to {str2}.",
            "The expression passed as 'expr' is not True.",
            "The expression passed as 'expr' is not False.",
            custom_err_msg,
            f"{str1} does not end with {end}.",
            f"{str1} does not contain {content}.",
            custom_err_msg,
            custom_err_msg,
            custom_err_msg,
            custom_err_msg
        ]
        exp_err_msg = "\n" + "\n".join(err_msgs)

        with self.assertRaises(AssertionError) as e:
            sa = SoftAssert()
            sa.assert_equal(str1, str2)
            sa.assert_true(False)
            sa.assert_false(False)
            sa.assert_false(True)
            sa.assert_that_text_starts_with(str1, "ing", custom_err_msg)
            sa.assert_that_text_ends_with(str1, end)
            sa.assert_that_text_contains(str1, content)
            sa.assert_that_list_is_empty(lst, custom_err_msg)
            sa.assert_that_list_is_not_empty([], custom_err_msg)
            sa.assert_that_list_has_item(lst, 2, custom_err_msg)
            sa.assert_that_list_contains_all(lst, [1, 2, 4, 5], custom_err_msg)
            sa.assert_all()

        self.assertEqual(exp_err_msg, str(e.exception))

    def test_asserts_handle_fail(self):
        with self.assertRaises(AssertionError):
            sa = SoftAssert()
            sa.handle(asserts.assert_equal, 1, 2)
            sa.handle(asserts.assert_equal, 2, 3)
            sa.handle(asserts.assert_equal, 4, 5, "custom message")
            sa.handle(asserts.assert_true, True)
            sa.handle(func=asserts.assert_equal, actual=2, exp=5, msg="custom message 2")
            sa.assert_all()

    def test_asserts_handle_pass(self):
        sa = SoftAssert()
        sa.handle(asserts.assert_equal, 2, 2)
        sa.handle(asserts.assert_equal, 4, 4)
        sa.handle(func=asserts.assert_equal, actual=5, exp=5, msg="custom message 2")
        sa.assert_all()

    def test_date_format(self):
        exp_date = "Jan 12, 2023 "
        exp_format = "%b %d, %Y %I:%M %p"
        assert_that_date_format_is(date=exp_date, exp_format=exp_format)


if __name__ == '__main__':
    unittest.main()
