# -*- coding: utf-8 -*-
import datetime, re
from gmun_tests import GmunTest
from gmun_tests.utils.vk import Vk
from time import sleep
from contextlib import suppress
import time
import random

from selenium.webdriver.common.keys import Keys
from anticaptchaofficial.recaptchav2proxyless import *
from anticaptchaofficial.recaptchav3proxyless import *
no_driver = False

silent = False

# pip3 install anticaptchaofficial

class Captcha(GmunTest):
    def __init__(self):
        self.name = 'Captcha'
        self.wait = 20
        GmunTest.__init__(self, no_driver, name=self.name)
        self.silent = silent or False




    def test(self, paused=True):
            try:
                test_start_time = datetime.now()
                driver = self.driver
                driver.set_page_load_timeout(30)
                self.dwait(self.wait)

                Vk.vk_login(self, user="79057324012", password="NMwdIdw32u", wait=5)

                for i in range(15):
                    url = f"https://vk.com/id{random.randint(10,9999999)}"
                    driver.get(url)
                    xpath = './/button[contains(text(), "Добавить в друзья")]'
                    if self.ifis_no_exception(xpath):
                        driver.find_element_by_xpath(xpath).click()
                        if self.ifis_no_exception('.//div[contains(text(), "Подтверждение действия")]'):
                            break
                sleep(1)
                # frame1 = ".//iframe[contains(@src, 'recaptcha/api2')]"
                # driver.switch_to.frame(self.find(frame1))
                # sleep(1)
                # self.find('.//span[@id="recaptcha-anchor"]').click()
                # sleep(1)
                # driver.switch_to.default_content()


                ANTICAPTCHA_KEY = "a9ba4752487faca9f61048a5bda25c62"
                iframe = self.find('.//iframe[contains(@src, "recaptcha")]').get_attribute("src")
                site_key_pattern = "\&k=.+?&"
                SITE_KEY = re.search(site_key_pattern, iframe)[0][3:-1]
                # SITE_KEY = '6Le00B8TAAAAACHiybbHy8tMOiJhM5vh88JVtP4c'

                PAGE_URL = url

                #
                # user_answer = NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(anticaptcha_key=ANTICAPTCHA_KEY) \
                #     .captcha_handler(websiteURL=PAGE_URL,
                #                      websiteKey=SITE_KEY)
                #
                # print(user_answer)
                # if type(user_answer) == dict and user_answer.get('solution') and user_answer.get('solution').get('gRecaptchaResponse'):
                #     solution = user_answer.get('solution').get('gRecaptchaResponse')

                solver = recaptchaV2Proxyless()
                solver.set_verbose(1)
                solver.set_key(ANTICAPTCHA_KEY)
                solver.set_website_url(url)
                solver.set_website_key(SITE_KEY)


                token = str(solver.solve_and_return_solution())
                # token = "111111111111111111111111111111111111111111"

                #    консоль браузера                ___grecaptcha_cfg.clients[0] и найти callback
                # ___grecaptcha_cfg.clients[0].V.V.callback
                # подробнее https://gist.github.com/2captcha/2ee70fa1130e756e1693a5d4be4d8c70
                # https://rucaptcha.com/api-rucaptcha#callback

                а = "___grecaptcha_cfg.clients[0].V.V.callback"
                driver.execute_script("document.getElementById('g-recaptcha-response').style.removeProperty('display');")
                driver.find_element_by_id('g-recaptcha-response').send_keys(token)
                driver.execute_script('___grecaptcha_cfg.clients[0].V.V.callback("{}")'.format(token))

                for i in range(15):
                    url = f"https://vk.com/id{random.randint(10,9999999)}"
                    driver.get(url)
                    xpath = './/button[contains(text(), "Добавить в друзья")]'
                    if self.ifis_no_exception(xpath):
                        driver.find_element_by_xpath(xpath).click()

                a=1

                # driver.find_element_by_id('recaptcha-demo-submit').submit()
                # frame2 = ".//iframe[contains(@title, 'проверка recaptcha')]"
                # driver.switch_to.frame(self.find(frame2))
                # driver.execute_script("document.getElementById('recaptcha-token').value='{}';".format(token))
                # driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML='{}';".format(token))
                # driver.execute_script("document.getElementById('g-recaptcha-response').value='{}';".format(token))
                # frame1 = ".//iframe[contains(@src, 'recaptcha/api2')]"
                # driver.switch_to.frame(self.find(frame1))
                # driver.execute_script("document.getElementById('recaptcha-token').type='{}';".format(''))
                # driver.find_element_by_xpath('.//button[@id="recaptcha-verify-button"]').click()
                # driver.find_element_by_xpath('.//*[@id="g-recaptcha-response"]')


                driver.quit()

            except Exception as e:
                print(e)


if __name__ == '__main__':
    for i in range(1):
        print("started at ", time.strftime('%H:%M:%S').replace("'", ""))
        try:
            test_obj = Captcha().test()
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")


