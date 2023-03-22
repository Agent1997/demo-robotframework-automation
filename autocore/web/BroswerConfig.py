from robot.api import logger
from selenium.webdriver.chrome.options import Options


def chrome_options(is_headless: bool = True):
    options: Options = Options()

    if is_headless:
        logger.info(msg="Setting browser to run in headless mode.")
        options.add_argument("--headless")
    else:
        logger.info(msg="Setting browser to run in UI mode.")

    options.add_argument("--no-sandbox")
    options.add_argument("--test-type")
    options.add_argument("use-fake-device-for-media-stream")
    options.add_argument("use-fake-ui-for-media-stream")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--incognito")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-extensions-file-access-check")
    options.add_argument("--disable-infobars")
    options.add_argument("--window-size=1920,1080")
    return options
