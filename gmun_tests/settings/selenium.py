import os, sys
import platform
from time import sleep
from selenium import webdriver
from gmun_tests.settings import HEADLESS


# SELENIUM_GRID_URL = 'http://d27.antipsy.ru:4444/wd/hub'

# CHROMEDRIVER_PATH = os.environ.get(
#     'CHROMEDRIVER_PATH',
#     os.sep.join([os.path.dirname(__file__), '..', '..', 'chromedriver', ])
# )

if platform.system() == 'Windows':
    CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH',
                                       os.sep.join([os.path.dirname(__file__), '..', '..', 'chromedriver.exe']))
else:
    CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH',
                                       os.sep.join([os.path.dirname(__file__), '..', '..', 'chromedriver']))


def config_profile(test_name):
    test_options = webdriver.ChromeOptions()
    if HEADLESS == 1:
        test_options.add_argument("--headless")
        test_options.add_argument("--disable-gpu")
    test_options.add_argument("--disable-extensions")
    test_options.add_argument("--disable-application-cache")
    test_options.add_argument("--disk-cache-size=5")
    test_options.add_argument("--media-cache-size=1")
    test_options.add_argument("--no-sandbox")
    test_options.add_argument('--enable-automation')
    test_options.add_argument('--ignore-certificate-errors')
    test_options.add_argument("--window-size=1200x900")
    test_options.add_argument("--disable-infobars")
    test_options.add_argument("--disable-dev-shm-usage")
    test_options.add_argument("--disable-browser-side-navigation")
    test_options.add_argument("--disable-features=VizDisplayCompositor")
    test_options.add_argument(f"user-data-dir=ChromeProfiles/{test_name}")
    test_options.page_load_strategy = 'normal'
    test_options.add_argument("--pageLoadStrategy=None")

    return test_options
