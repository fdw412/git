from selenium.common.exceptions import NoSuchElementException
import requests, time, json, random
from time import sleep
from contextlib import suppress
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from gmun_tests.settings import SCREENSHOT_PATH, SCREENSHOT_TIME_FORMAT
import datetime


def vk_login(driver, inter_result, implicitly_wait):

    def is_element_present(how, what):
        try:
            driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True


    sleep(1)
    for i in range(0,2):
        try:
            driver.implicitly_wait(10)
            driver.maximize_window()
            driver.get(f"https://vk.com")

            # проверяем на странице наличие элемента "Моя страница", если есть, то ok, если нет, то то логинимся в Вк
            if is_element_present(By.XPATH, ".//span[contains(text(), 'Моя страница')]"):
                text = "vk login ok, "
                inter_result['comment'] += text
                break
            else:
                if is_element_present(By.XPATH, ".//button[@id='index_login_button']") == True:
                    driver.find_element_by_xpath(".//input[@id='index_email']").send_keys()
                    sleep(1)
                    driver.find_element_by_xpath(".//input[@id='index_pass']").send_keys("")
                    driver.find_element_by_xpath(".//button[@id='index_login_button']").click()
                    sleep(1)
                    driver.refresh()
                    text="vk login ok, "
                    inter_result['comment'] += text
                    break
                else:
                    if i == 1:
                        inter_result['result'] = 1
                        text="vk login fail не удалось найти кнопку входа во время загрузки vk.com, "
                        inter_result['comment'] += text
                        inter_result['error'] += text
                        screenshot = f"{SCREENSHOT_PATH}\\{datetime.datetime.now().strftime({SCREENSHOT_TIME_FORMAT})}.png"
                        driver.save_screenshot(screenshot)
                        inter_result['screen_paths'].append(screenshot)
                        print(inter_result['error'])

        except Exception as e:
            inter_result['result'] = 1
            text = f'vk login fail, {str(e)}'
            inter_result['comment'] += text
            inter_result['error'] += text
            screenshot = f"{SCREENSHOT_PATH}\\{datetime.datetime.now().strftime({SCREENSHOT_TIME_FORMAT})}.png"
            driver.save_screenshot(screenshot)
            inter_result['screen_paths'].append(screenshot)
            print(inter_result['error'])
            driver.implicitly_wait(implicitly_wait)

        driver.implicitly_wait(implicitly_wait)

    return inter_result