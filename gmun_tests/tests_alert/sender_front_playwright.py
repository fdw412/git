# -*- coding: utf-8 -*-
import datetime
from gmun_tests.settings import user_id, app_id_dev, app_id_prod
from gmun_tests import GmunTest
from gmun_tests.utils.vk import Vk
from gmun_tests.utils.mattermost import Mattermost
from contextlib import suppress
from time import sleep
import time
from gmun_tests.settings.test_run_params import test_run_params
from selenium.webdriver.common.by import By

# python -m playwright codegen - консоль питона

# >>> from playwright import sync_playwright
# >>> pw = sync_playwright().start()
# >>> browser = pw.chromium.launch(headless=False, executablePath='/Applications/Microsoft



def ifis(xpath, wait=None):
    if not wait:
        wait = 700
    page.setDefaultTimeout(wait)
    try:
        page.waitForSelector(xpath)
        return True
    except TimeoutError:
        return False
    page.setDefaultTimeout(30000)

from playwright import sync_playwright
from playwright import TimeoutError
playwright = sync_playwright().start()
browser = playwright.chromium.launchPersistentContext(headless=False, userDataDir='ChromeProfiles/playwrite')
page = browser.pages[0]
page.setDefaultTimeout(30000)

page.goto("https://vk.com/")
if ifis("//button[@id='index_login_button']"):
    page.fill("form[id='index_login_form'] input[name='email']", "")
    page.fill("form[id=\"index_login_form\"] input[name=\"pass\"]", "")
    page.press("//button[@id='index_login_button']", "Enter")
# page.waitForSelector('//input[@id="index_email888888888888"]')
a=1





page.close()
context.close()
browser.close()
playwright.stop()








