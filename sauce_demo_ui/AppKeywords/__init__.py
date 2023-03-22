from SeleniumLibrary import SeleniumLibrary
from robot.api.deco import library
from robotlibcore import DynamicCore

from sauce_demo_ui.AppKeywords.ActionKeywords import ActionKeywords
from sauce_demo_ui.AppKeywords.BrowserKeywords import BrowserKeywords
from sauce_demo_ui.AppKeywords.ValidationKeywords import ValidationKeywords


@library(scope='GLOBAL')
class AppKeywords(DynamicCore):

    def __init__(self, headless: bool = True):
        se_lib = SeleniumLibrary()
        keywords = [
            ActionKeywords(se_lib=se_lib),
            BrowserKeywords(se_lib=se_lib, headless=headless),
            ValidationKeywords(se_lib=se_lib)
        ]

        DynamicCore.__init__(self, keywords)
