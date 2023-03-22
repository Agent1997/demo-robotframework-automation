from typing import Any

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError


def set_test_variable(name, value):
    try:
        BuiltIn().set_test_variable(name, value)
    except RobotNotRunningError as e:
        logger.warn(f"Variable: {name} with value {value} not set as test variable due to {str(e)}.")


def set_suite_variable(name, value):
    try:
        BuiltIn().set_suite_variable(name, value)
    except RobotNotRunningError as e:
        logger.warn(f"Variable: {name} with value {value} not set as test variable due to {str(e)}.")


def get_variable_value(name, r_except: bool = True, default: Any = None):
    try:
        value = BuiltIn().get_variable_value(name=name, default=default)

        if value is None and r_except:
            raise Exception(f"Variable with name {name} not found.")

        return value
    except RobotNotRunningError as e:
        logger.warn(f"Can't get variable with name {name} due to {str(e)}.")
        return default


def set_global_variable(name, value):
    try:
        BuiltIn().set_global_variable(name, value)
    except RobotNotRunningError as e:
        logger.warn(f"Variable: {name} with value {value} not set as test variable due to {str(e)}.")
