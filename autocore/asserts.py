"""
Provides Hard and Soft Assertion capability. Wraps robot.api.logger
"""
from datetime import datetime

from robot.api import logger
from robot.utils import asserts


def assert_that_date_format_is(date: str, exp_format: str, msg: str = None, s_msg: str = None):
    """Fail the test if the ``date`` provided does not match the ``exp_format``."""
    err_msg = f"Expecting format of {date} to match format {exp_format} but it did not."
    if msg is not None:
        err_msg = msg

    try:
        datetime.strptime(date, exp_format)
        if s_msg is not None:
            logger.info(msg=s_msg)
        else:
            logger.info(msg=f"Verified that date string {date} match the format {exp_format}.")
    except Exception:
        raise AssertionError(err_msg)


def assert_equal(actual, exp, msg: str = None, s_msg: str = None):
    """Fail if ``actual`` and ``exp`` are unequal as determined by the '==' operator.

    If ``msg`` was provided, this will be the error message in case this keyword failed.

    Examples:
        assert_equal(1,2) -> fail \n
        assert_equal("one","two") -> fail \n
        assert_equal(1,2, "one is not equal to two") -> fail \n
        assert_equal(1,1) -> pass \n
        assert_equal("one","one", "error message if this keyword fails") -> pass
    """
    if msg is None:
        msg = "{0} is not equal to {1}.".format(actual, exp)
    try:
        asserts.assert_equal(actual, exp, msg)
    except AssertionError:
        raise AssertionError(msg)
    else:
        if s_msg is not None:
            logger.info(msg=s_msg)
        else:
            logger.info("Verified that: {0} is equal to {1}.".format(actual, exp), also_console=True)


def fail(msg=None):
    """Fail test immediately with the given message.

    If ``msg`` was provided, this will be the error message.

    Examples:
        fail() -> fail \n
        fail("error message to be displayed") -> fail
    """
    if msg is None:
        msg = "Fail Test."
    try:
        asserts.fail(msg)
    except AssertionError:
        raise AssertionError(msg)


def assert_true(expr, msg=None, s_msg: str = None):
    """Fail the test unless the provided ``expr`` is True.

    If ``msg`` was provided, this will be the error message in case this keyword failed.

    Examples:
        assert_true(1 != 1) -> fail \n
        assert_true([]) -> fail since empty lists are falsy \n
        assert_true("string" == "String", "Custom error message") -> fail \n
        assert_true(1,1) -> pass \n
        assert_true([1,2,3], "Custom error message") -> pass since list with contents are truth
    """
    if msg is None:
        msg = "The expression passed as 'expr' is not True."

    try:
        asserts.assert_true(expr, msg)
    except AssertionError:
        raise AssertionError(msg)
    else:
        if s_msg is not None:
            logger.info(msg=s_msg)
        else:
            logger.info("Verified that expression passed as 'expr' is True.", also_console=True)


def assert_false(expr, msg=None, s_msg: str = None):
    """Fail the test unless the provided ``expr`` is False.

    If ``msg`` was provided, this will be the error message in case this keyword failed.

    Examples:
        assert_false(1 == 1) -> fail since 1 the expression is True and the method expects False \n
        assert_false(5 > 1, "Customer error message") -> fail \n
        assert_false(False) -> pass
    """
    if msg is None:
        msg = "The expression passed as 'expr' is not False."
    try:
        asserts.assert_false(expr, msg)
    except AssertionError:
        raise AssertionError(msg)
    else:
        if s_msg is not None:
            logger.info(msg=s_msg)
        else:
            logger.info("Verified that the expression passed as 'expr' is False.", also_console=True)


def assert_that_text_is_not_empty(txt: str, msg: str = None, s_msg: str = None):
    """Fail the test if the given ``txt`` is empty. len(txt) == 0 .

    If ``msg`` was provided, this will be the error message in case this keyword failed.

    Examples:
        assert_that_text_is_not_empty("")  -> fail  \n
        assert_that_text_is_not_empty(" ")  -> pass since string has space  \n
        assert_that_text_is_not_empty("text")  -> pass \n
    """
    if msg is None:
        msg = f"Provided text is empty."

    if (txt is None) or len(txt) == 0:
        fail(msg)
    else:
        if s_msg is not None:
            logger.info(msg=s_msg)
        else:
            logger.info(f"Verified that provided text: {txt} is not empty.", also_console=True)


def assert_that_text_starts_with(txt: str, start: str, msg=None, s_msg: str = None):
    """Fail the test if the given ``txt`` does not start with ``start``. This is case-sensitive.

    If ``msg`` was provided, this will be the error message in case this keyword failed.

    Examples:
        assert_that_text_starts_with("String", "ing") -> fail   \n
        assert_that_text_starts_with("String", "ing", "Custom error message.") -> fail  \n
        assert_that_text_starts_with("String", "str") -> fail since this is case-sensitive  \n
        assert_that_text_starts_with("String", "Str") -> pass
    """
    if msg is None:
        msg = "{0} does not start with {1}.".format(txt, start)

    if not txt.startswith(start):
        fail(msg)
    else:
        if s_msg is not None:
            logger.info(msg=s_msg)
        else:
            logger.info("Verified that: {0} starts with {1}.".format(txt, start), also_console=True)


def assert_that_text_ends_with(txt: str, end: str, msg=None, s_msg: str = None):
    """Fail the test if the given ``txt`` does not end with ``end``. This is case-sensitive.

    If ``msg`` was provided, this will be the error message in case this keyword failed.

    Examples:
        assert_that_text_ends_with("String","rin") -> fail \n
        assert_that_text_ends_with("String","ING","Custom error message") -> fail \n
        assert_that_text_ends_with("String","ing") -> pass
    """
    if msg is None:
        msg = "{0} does not end with {1}.".format(txt, end)

    if not txt.endswith(end):
        fail(msg)
    else:
        if s_msg is not None:
            logger.info(msg=s_msg)
        else:
            logger.info("Verified that: {0} ends with {1}.".format(txt, end), also_console=True)


def assert_that_text_contains(txt: str, content: str, msg=None, s_msg: str = None):
    """Fail the test if the given ``txt`` does not contain ``content``. This is case-sensitive.

    If ``msg`` was provided, this will be the error message in case this keyword failed.

    Examples:
        assert_that_text_contains("String","sng") -> fail \n
        assert_that_text_contains("String,"trg","Custom error message") -> fail \n
        assert_that_text_contains("String","Ing") -> fail since this is case-sensitive  \n
        assert_that_text_contains("String","tri") -> pass
    """
    if msg is None:
        msg = "{0} does not contain {1}.".format(txt, content)

    if not (content in txt):
        fail(msg)
    else:
        if s_msg is not None:
            logger.info(msg=s_msg)
        else:
            logger.info("Verified that: {0} contains {1}.".format(txt, content), also_console=True)


def assert_that_list_is_empty(lst: list, msg=None, s_msg: str = None):
    """Fail the test if the given ``lst`` is not empty. This accepts list of Any type.

    If ``msg`` was provided, this will be the error message in case this keyword failed.

    Examples:
        assert_that_list_is_empty([1,2,3]) -> fail \n
        assert_that_list_is_empty(["one","two","three"], "Custom error message") -> fails \n
        assert_that_list_is_empty([]) -> pass
    """
    if msg is None:
        msg = "List {0} is not empty.".format(lst)

    if len(lst) > 0:
        fail(msg)
    else:
        if s_msg is not None:
            logger.info(msg=msg)
        else:
            logger.info("Verified that: list {0} is empty.".format(lst), also_console=True)


def assert_that_list_is_not_empty(lst: list, msg=None, s_msg: str = None):
    """Fail the test if the given ``lst`` is empty. This accepts list of Any type.

    If ``msg`` was provided, this will be the error message in case this keyword failed.

    Examples:
        assert_that_list_is_not_empty([]) -> fail \n
        assert_that_list_is_not_empty([], "Custom error message") -> fail \n
        assert_that_list_is_not_empty([1,2,3], "Custom error message") -> pass \n
        assert_that_list_is_not_empty(["One","Two","Three"]) -> pass
    """
    if msg is None:
        msg = "List {0} is empty.".format(lst)

    if len(lst) == 0:
        fail(msg)
    else:
        if s_msg is not None:
            logger.info(msg=s_msg)
        else:
            logger.info("Verified that: list {0} is not empty.".format(lst), also_console=True)


def assert_that_list_has_item(lst: list, content, msg=None, s_msg: str = None):
    """Fail the test if the given ``lst`` does not contain the provided ``content``.

    If ``msg`` was provided, this will be the error message in case this keyword failed.

    Examples:
        assert_that_list_has_item([1,2,4], 3) -> fail since 3 is not in [1,2,4] \n
        assert_that_list_has_item([1,2,4], 3, "Custom Error Message") -> fail \n
        assert_that_list_has_item([1,2,4], 4) -> pass
    """
    if msg is None:
        msg = "List {0} does not contain {1}.".format(lst, content)
    if not (content in lst):
        fail(msg)
    else:
        if s_msg is not None:
            logger.info(msg=s_msg)
        else:
            logger.info("Verified that: list {0} contains {1}.".format(lst, content), also_console=True)


def assert_that_list_does_not_contain(lst: list, item, msg=None, s_msg: str = None):
    """Fail the test if the given ``lst`` contains the provided ``item``.

    If ``msg`` was provided, this will be the error message in case this keyword failed.

    Examples:
        assert_that_list_does_not_contain([1,2,3,4], 2) -> fail since 2 is in the list
        assert_that_list_does_not_contain([1,2,3,4], 10) -> pass since 10 is not in the list.
    """
    if msg is None:
        msg = f"List {lst} contains {item}."

    if item in lst:
        fail(msg)
    else:
        if s_msg is not None:
            logger.info(msg=s_msg)
        else:
            logger.info(f"Verified that list {lst} does not contain {item}.", also_console=True)


def assert_that_list_contains_all(lst: list, contents: list, msg=None, s_msg: str = None):
    """Fail the test if the given ``lst`` does not contain all ``contents``.

    If ``msg`` was provided, this will be the error message in case this keyword failed.

    Examples:
        assert_that_list_contains_all([1,2,3,4,5], [1,2,7]) -> fail since 7 is not in [1,2,3,4,5]   \n
        assert_that_list_contains_all([1,2,3,4,5],[6,7,8], "Custom error message") -> fail  \n
        assert_that_list_contains_all([1,2,3,4,5],[1,2,3]) -> pass
    """
    missing_items = []

    for i in contents:
        if not (i in lst):
            missing_items.append(i)

    if len(missing_items) > 0:
        if msg is None:
            msg = "List {0} does not contain all of {1}. See missing item/s: {2}.".format(lst, contents, missing_items)
        fail(msg)
    else:
        if s_msg is not None:
            logger.info(msg=s_msg)
        else:
            logger.info("Verified that: list {0} contains all of {1}.".format(lst, contents), also_console=True)


class SoftAssert:
    """Provide the capability to perform Soft Assertions. Fail if at least one prior assertions failed.

    NOTE: Always call assert_all() at the end, otherwise failures (if there are) will not be reported resulting
    to a passed test even if it's not.

    Example:
        sa = SoftAssert()   \n
        sa.assert_equal(1,2) -> fail but next assertion will still be executed \n
        sa.assert_equal("one","two") -> fail but next assertion will still be executed \n
        sa.assert_all()
    """

    def __init__(self):
        self.__errors: list[str] = []

    def handle(self, func, *args, **kwargs):
        """Use this to convert hard asserts to soft asserts."""
        try:
            func(*args, **kwargs)
        # except AssertionError as e:
        except Exception as e:
            self.__errors.append(str(e))

    def assert_equal(self, actual, exp, msg: str = None, s_msg: str = None):
        """Fail if ``actual`` and ``exp`` are unequal as determined by the '==' operator.

        If ``msg`` was provided, this will be the error message in case this keyword failed.

        Example:
            sa = SoftAssert() \n
            sa.assert_equal(1,2) -> fail \n
            sa.assert_equal("one","two") -> fail \n
            sa.assert_equal(1,2, "one is not equal to two") -> fail \n
            sa.assert_equal(1,1) -> pass \n
            sa.assert_equal("one","one", "error message if this keyword fails") -> pass \n
            sa.assert_all()
        """
        try:
            assert_equal(actual, exp, msg=msg, s_msg=s_msg)
        except AssertionError as e:
            if msg is None:
                msg = str(e)
            self.__errors.append(msg)

    def assert_true(self, expr, msg=None, s_msg: str = None):
        """Fail the test unless the provided ``expr`` is True.

        If ``msg`` was provided, this will be the error message in case this keyword failed.

        Examples:
            sa = SoftAssert() \n
            sa.assert_true(1 != 1) -> fail \n
            sa.assert_true([]) -> fail since empty lists are falsy \n
            sa.assert_true("string" == "String", "Custom error message") -> fail \n
            sa.assert_true(1,1) -> pass \n
            sa.assert_true([1,2,3], "Custom error message") -> pass since list with contents are truth \n
            sa.assert_all()
        """
        try:
            assert_true(expr, msg, s_msg=s_msg)
        except AssertionError as e:
            if msg is None:
                msg = str(e)
            self.__errors.append(msg)

    def assert_false(self, expr, msg=None, s_msg: str = None):
        """Fail the test unless the provided ``expr`` is False.

        If ``msg`` was provided, this will be the error message in case this keyword failed.

        Examples:
            sa = SoftAssert()   \n
            sa.assert_false(1 == 1) -> fail since 1 the expression is True and the method expects False \n
            sa.assert_false(5 > 1, "Customer error message") -> fail \n
            sa.assert_false(False) -> pass \n
            sa.assert_all()
        """
        try:
            assert_false(expr, msg, s_msg=s_msg)
        except AssertionError as e:
            if msg is None:
                msg = str(e)
            self.__errors.append(msg)

    def assert_that_text_is_not_empty(self, txt: str, msg: str = None, s_msg: str = None):
        """Fail the test if the given ``txt`` is empty. len(txt) == 0 .

        If ``msg`` was provided, this will be the error message in case this keyword failed.

        Examples:
            sa = SoftAssert()   \n
            sa.assert_that_text_is_not_empty("")  -> fail  \n
            sa.assert_that_text_is_not_empty(" ")  -> pass since string has space  \n
            sa.assert_that_text_is_not_empty("text")  -> pass \n
            sa.assert_all()
        """
        try:
            assert_that_text_is_not_empty(txt, msg, s_msg=s_msg)
        except AssertionError as e:
            if msg is None:
                msg = str(e)
            self.__errors.append(msg)

    def assert_that_text_starts_with(self, txt: str, start: str, msg=None, s_msg: str = None):
        """Fail the test if the given ``txt`` does not start with ``start``. This is case-sensitive.

        If ``msg`` was provided, this will be the error message in case this keyword failed.

        Examples:
            sa = SoftAssert()   \n
            sa.assert_that_text_starts_with("String", "ing") -> fail   \n
            sa.assert_that_text_starts_with("String", "ing", "Custom error message.") -> fail  \n
            sa.assert_that_text_starts_with("String", "str") -> fail since this is case-sensitive  \n
            sa.assert_that_text_starts_with("String", "Str") -> pass   \n
            sa.assert_all()
        """
        try:
            assert_that_text_starts_with(txt, start, msg, s_msg=s_msg)
        except AssertionError as e:
            if msg is None:
                msg = str(e)
            self.__errors.append(msg)

    def assert_that_text_ends_with(self, txt: str, end: str, msg=None, s_msg: str = None):
        """Fail the test if the given ``txt`` does not end with ``end``. This is case-sensitive.

        If ``msg`` was provided, this will be the error message in case this keyword failed.

        Examples:
            sa = SoftAssert()
            sa.assert_that_text_ends_with("String","rin") -> fail \n
            sa.assert_that_text_ends_with("String","ING","Custom error message") -> fail \n
            sa.assert_that_text_ends_with("String","ing") -> pass \n
            sa.assert_all()
        """
        try:
            assert_that_text_ends_with(txt, end, msg, s_msg=s_msg)
        except AssertionError as e:
            if msg is None:
                msg = str(e)
            self.__errors.append(msg)

    def assert_that_text_contains(self, txt: str, content: str, msg=None, s_msg: str = None):
        """Fail the test if the given ``txt`` does not contain ``content``. This is case-sensitive.

        If ``msg`` was provided, this will be the error message in case this keyword failed.

        Examples:
            sa = SoftAssert()   \n
            sa.assert_that_text_contains("String","sng") -> fail \n
            sa.assert_that_text_contains("String,"trg","Custom error message") -> fail \n
            sa.assert_that_text_contains("String","Ing") -> fail since this is case-sensitive  \n
            sa.assert_that_text_contains("String","tri") -> pass    \n
            sa.assert_all()
        """
        try:
            assert_that_text_contains(txt, content, msg, s_msg=s_msg)
        except AssertionError as e:
            if msg is None:
                msg = str(e)
            self.__errors.append(msg)

    def assert_that_list_is_empty(self, lst: list, msg=None, s_msg: str = None):
        """Fail the test if the given ``lst`` is not empty. This accepts list of Any type.

        If ``msg`` was provided, this will be the error message in case this keyword failed.

        Examples:
            sa = SoftAssert()   \n
            sa.assert_that_list_is_empty([1,2,3]) -> fail \n
            sa.assert_that_list_is_empty(["one","two","three"], "Custom error message") -> fails \n
            sa.assert_that_list_is_empty([]) -> pass    \n
            sa.assert_all()
        """
        try:
            assert_that_list_is_empty(lst, msg, s_msg=s_msg)
        except AssertionError as e:
            if msg is None:
                msg = str(e)
            self.__errors.append(msg)

    def assert_that_list_is_not_empty(self, lst: list, msg=None, s_msg: str = None):
        """Fail the test if the given ``lst`` is empty. This accepts list of Any type.

        If ``msg`` was provided, this will be the error message in case this keyword failed.

        Examples:
            sa = SoftAssert()   \n
            sa.assert_that_list_is_not_empty([]) -> fail \n
            sa.assert_that_list_is_not_empty([], "Custom error message") -> fail \n
            sa.assert_that_list_is_not_empty([1,2,3], "Custom error message") -> pass \n
            sa.assert_that_list_is_not_empty(["One","Two","Three"]) -> pass \n
            sa.assert_all()
        """
        try:
            assert_that_list_is_not_empty(lst, msg, s_msg=s_msg)
        except AssertionError as e:
            if msg is None:
                msg = str(e)
            self.__errors.append(msg)

    def assert_that_list_has_item(self, lst: list, content, msg=None, s_msg: str = None):
        """Fail the test if the given ``lst`` does not contain the provided ``content``.

        If ``msg`` was provided, this will be the error message in case this keyword failed.

        Examples:
            sa = SoftAssert()   \n
            sa.assert_that_list_has_item([1,2,4], 3) -> fail since 3 is not in [1,2,4] \n
            sa.assert_that_list_has_item([1,2,4], 3, "Custom Error Message") -> fail \n
            sa.assert_that_list_has_item([1,2,4], 4) -> pass    \n
            sa.assert_all()
        """
        try:
            assert_that_list_has_item(lst, content, msg, s_msg=s_msg)
        except AssertionError as e:
            if msg is None:
                msg = str(e)
            self.__errors.append(msg)

    def assert_that_list_does_not_contain(self, lst: list, item, msg=None, s_msg: str = None):
        """Fail the test if the given ``lst`` contains the provided ``item``.

        If ``msg`` was provided, this will be the error message in case this keyword failed.

        Examples:
            sa = SoftAssert()   \n
            sa.assert_that_list_does_not_contain([1,2,3,4], 2) -> fail since 2 is in the list
            sa.assert_that_list_does_not_contain([1,2,3,4], 10) -> pass since 10 is not in the list.
            sa.assert_all()
        """
        try:
            assert_that_list_does_not_contain(lst, item, msg, s_msg=s_msg)
        except AssertionError as e:
            if msg is None:
                msg = str(e)
            self.__errors.append(msg)

    def assert_that_list_contains_all(self, lst: list, contents: list, msg=None, s_msg: str = None):
        """Fail the test if the given ``lst`` does not contain all ``contents``.

        If ``msg`` was provided, this will be the error message in case this keyword failed.

        Examples:
            sa = SoftAssert()   \n
            sa.assert_that_list_contains_all([1,2,3,4,5], [1,2,7]) -> fail since 7 is not in [1,2,3,4,5]   \n
            sa.assert_that_list_contains_all([1,2,3,4,5],[6,7,8], "Custom error message") -> fail  \n
            sa.assert_that_list_contains_all([1,2,3,4,5],[1,2,3]) -> pass  \n
            sa.assert_all()
        """
        try:
            assert_that_list_contains_all(lst, contents, msg, s_msg=s_msg)
        except AssertionError as e:
            if msg is None:
                msg = str(e)
            self.__errors.append(msg)

    def assert_that_date_format_is(self, date: str, exp_format: str, msg=None, s_msg: str = None):
        """Fail the test if the ``date`` provided does not match the ``exp_format``."""
        try:
            assert_that_date_format_is(date=date, exp_format=exp_format, msg=msg, s_msg=s_msg)
        except AssertionError as e:
            if msg is None:
                msg = str(e)
            self.__errors.append(msg)

    def assert_all(self):
        """Will fail test if at least one of the prior assertions has failed."""
        if len(self.__errors) > 0:
            err_msg = "\n" + "\n".join(self.__errors)
            raise AssertionError(err_msg)
