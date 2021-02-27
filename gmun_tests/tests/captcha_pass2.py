# -*- coding: utf-8 -*-
import re
from gmun_tests.utils.vk import Vk
from time import sleep
import random
from selenium import webdriver
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.common.exceptions import NoSuchElementException
import os


def ifis(xpath):
    driver.implicitly_wait(0.5)
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException as e:
        driver.implicitly_wait(30)
        return False
    return True

CHROMEDRIVER_PATH = os.sep.join([os.path.dirname(__file__), '..', '..', 'chromedriver.exe'])

driver = webdriver.Chrome(CHROMEDRIVER_PATH)


driver.maximize_window()
driver.set_page_load_timeout(30)

driver.implicitly_wait(5)
driver.get(f"https://vk.com")
sleep(1)
if ifis(".//span[contains(text(), 'Моя страница')]"):
    pass
else:
    if ifis(".//button[@id='index_login_button']") == True:
        driver.find_element_by_xpath(".//input[@id='index_email']").send_keys(79057324012)
        driver.find_element_by_xpath(".//input[@id='index_pass']").send_keys("NMwdIdw32u")
        driver.find_element_by_xpath(".//button[@id='index_login_button']").click()
        sleep(2)
        driver.refresh()

for i in range(15):
    driver.implicitly_wait(5)
    url = f"https://vk.com/id{random.randint(10,9999999)}"
    driver.get(url)
    xpath = './/button[contains(text(), "Добавить в друзья")]'
    driver.implicitly_wait(0.5)
    if ifis(xpath):
        driver.find_element_by_xpath(xpath).click()
        if ifis('.//div[contains(text(), "Подтверждение действия")]'):
            break
sleep(1)


ANTICAPTCHA_KEY = "a9ba4752487faca9f61048a5bda25c62"
iframe = driver.find_element_by_xpath('.//iframe[contains(@src, "recaptcha")]').get_attribute("src")
site_key_pattern = "\&k=.+?&"
SITE_KEY = re.search(site_key_pattern, iframe)[0][3:-1]
PAGE_URL = url


solver = recaptchaV2Proxyless()
solver.set_verbose(1)
solver.set_key(ANTICAPTCHA_KEY)
solver.set_website_url(url)
solver.set_website_key(SITE_KEY)


token = str(solver.solve_and_return_solution())
driver.execute_script("document.getElementById('g-recaptcha-response').style.removeProperty('display');")
driver.find_element_by_id('g-recaptcha-response').send_keys(token)
driver.execute_script('___grecaptcha_cfg.clients[0].V.V.callback("{}")'.format(token))

for i in range(15):
    url = f"https://vk.com/id{random.randint(10,9999999)}"
    driver.get(url)
    xpath = './/button[contains(text(), "Добавить в друзья")]'
    if ifis(xpath):
        driver.find_element_by_xpath(xpath).click()

driver.quit()

