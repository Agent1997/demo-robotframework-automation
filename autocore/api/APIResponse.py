from typing import Any

from jsonpath_ng.ext import parse
from requests import Response

from autocore.asserts import *


class APIResponse:

    def __init__(self, response: Response):
        self.__response = response

    @property
    def response(self) -> Response:
        return self.__response

    def status_code_should_be(self, exp: int):
        act = self.__response.status_code
        assert_equal(act, exp, msg=f"Expecting status code to be {exp} but got {act}")

    def get_header_value(self, key: str):
        return self.__response.headers[key]

    def header_value_of_should_be(self, key: str, exp: str):
        act = self.__response.headers[key]
        assert_equal(act, exp, f"Expecting value of header {key} to be {exp} but got {act}")

    def get_value_of(self, json_path: str) -> Any:
        return self.__execute(json_path)

    def value_of_should_be(self, json_path: str, exp_value: Any, msg: str = None):
        act_value = self.__execute(json_path)

        if len(act_value) > 1:
            raise Exception(
                f"Expecting Json path: {json_path} to point to a unique value but is not. Consider refining the json path.")

        if len(act_value) == 0:
            raise Exception(f"No value found using Json path: {json_path}. Consider refining the json path.")

        if msg is None:
            msg = f"Expecting  value of {json_path} to be {exp_value} but got {act_value}."
        assert_equal(act_value[0], exp_value, msg)

    def list_of_should_contain(self, json_path: str, exp_value: Any, msg: str = None):
        act_value = self.__execute(json_path)

        if len(act_value) == 0:
            raise Exception(f"No value found using Json path: {json_path}. Consider refining the json path.")

        if msg is None:
            msg = f"Jsonpath: {json_path}. Expecting list of {act_value} to contain {exp_value}."

        assert_that_list_has_item(act_value, exp_value, msg)

    def list_of_should_not_contain(self, json_path: str, exp_value: Any, msg: str = None):
        act_value = self.__execute(json_path)

        if len(act_value) == 0:
            raise Exception(f"No value found using Json path: {json_path}. Consider refining the json path.")

        if msg is None:
            msg = f"Jsonpath: {json_path}. Expecting list of {act_value} to NOT contain {act_value}."

        assert_that_list_does_not_contain(act_value, exp_value, msg)

    def __execute(self, query: str) -> Any:
        query = parse(query)
        return [match.value for match in query.find(self.__response.json())]
