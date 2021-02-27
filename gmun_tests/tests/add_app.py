# -*- coding: utf-8 -*-
import datetime
import os
from gmun_tests.settings import logger
from gmun_tests.settings import TOKEN_USER
from gmun_tests.settings import token_ms_chain_2020_gid_191083897
from gmun_tests import GmunTest
from gmun_tests.utils.vk import Vk
from gmun_tests.utils.mattermost import Mattermost
from time import sleep
from contextlib import suppress
import time
import random
from gmun_tests.settings.test_run_params import test_run_params
from selenium.webdriver.common.keys import Keys


gid = 172321382
uid=585675
no_driver = False
silent = True

class Add_app(GmunTest):
    def __init__(self):
        self.name = 'Add_app'
        self.t_check = test_run_params[f'{self.name}']['t_check']
        self.run_series_count = test_run_params[f'{self.name}']['run_series_count']
        self.fail_limit_count = test_run_params[f'{self.name}']['fail_limit_count']
        self.mattermost = Mattermost()
        self.wait = 30
        GmunTest.__init__(self, no_driver, name=self.name)
        self.silent = silent or False

    def test(self, paused=True):
            if not self.redis.get(self.name) == None:
                self.get_result()
            else:
                self.inter_result["result"] = 0
                self.set_result()

            # list_temp=[]
            # for i in self.redis_results_chain:
            #     list_temp.append(datetime.datetime.fromtimestamp(int(i[2:])))

            a = self.redis_results_chain[0]
            b = datetime.datetime.fromtimestamp(int(a[2:]))
            now = datetime.datetime.now()

            c = round(abs((now - b).total_seconds() / 3600))
            if c < 0:
                print("время с прошлого теста меньше 24 часов")
            else:
                try:
                    test_start_time = datetime.datetime.now()
                    driver = self.driver
                    driver.set_page_load_timeout(30)
                    driver.implicitly_wait(self.wait)

                    def find(path):
                        a = self.driver.find_element_by_xpath(path)
                        return a

                    Vk.vk_login(self, self.wait, user=919957956946, password="TwDzWjq9Td")
                    id = random.randint(1, 1000000)
                    name = f'автотест добавления приложения {id}'
                    # self.find('//*[contains(text(), "Сообщества")]')

                    i = 1
                    cycle_count_limit = 2
                    self.dwait(self.wait)

                    while i <= cycle_count_limit:
                        try:
                            driver.get(f"https://vk.com/groups?w=groups_create")
                            sleep(3)
                            self.if_click('//*[contains(text(), "Бизнес")]', "", f"Не нашел надпись Бизнес, попытка {i}")
                            sleep(1)
                            self.find('.//input[@id="groups_create_box_title"]').send_keys(name, Keys.ENTER)
                            sleep(1)
                            self.find('//input[@class ="selector_input"]').click()
                            sleep(1)
                            self.if_click('//*[contains(text(), "Автопроизводитель")]', "", "Не нашел Автопроизводитель")

                            if self.ifis_no_exception('//button[contains(text(), "Создать сообщество")]'):
                                self.if_click('//button[contains(text(), "Создать сообщество")]', "", f"Не нашел надпись Создать сообщество, попытка {i}")
                            sleep(3)
                            driver.get("https://vk.com/groups")
                            sleep(1)
                            for j in range(4):
                                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                                sleep(1)
                            self.dwait(3)
                            if self.ifis_no_exception(f'//a[contains(text(), "{name}")]'):
                                url = self.find(f'//a[contains(text(), "{name}")]').get_attribute("href")
                                self.dwait(self.wait)
                                break
                            else:
                                if i == cycle_count_limit:
                                    self.pars_err(
                                        f"Скрипт не смог создать новое сообщество при нажатии на  за \"Создать сообщество\" за {i} попыток")
                                    break
                                sleep(10)
                                i += 1
                                driver.refresh()
                        except Exception as e:
                            pass

                    sleep(1)
                    # url = driver.current_url
                    driver.get(f"{url}?act=messages")
                    sleep(1)
                    self.find('//*[contains(text(), "Отключены")]').click()
                    sleep(2)
                    self.find('//*[contains(text(), "Включены")]').click()
                    sleep(2)
                    self.find('//*[contains(text(), "Сохранить")]').click()
                    sleep(1)
                    driver.get(f"{url}?act=apps")
                    sleep(1)
                    self.find('//div/a[contains(text(), "Гамаюн")]/../a/../../../div/a').click()
                    sleep(1)
                    with suppress (Exception):
                        self.dwait(2)
                        driver.find_element_by_xpath('//button[contains(text(), "Добавить")]').click()
                        self.dwait(self.wait)

                    self.find('//*[contains(text(), "Настроить приложение")]').click()
                    sleep(8)
                    Vk.get_frame(self)

                    i = 1
                    cycle_count_limit = 3
                    self.dwait(self.wait)
                    while i <= cycle_count_limit:
                        self.dwait(self.wait)
                        if self.ifis_no_exception('//*[contains(text(), "Начать работу")]'):
                            self.find('//*[contains(text(), "Начать работу")]').click()
                            sleep(2)
                            driver.switch_to.default_content()
                            sleep(1)
                            self.find('//button[contains(text(), "Разрешить")]').send_keys(Keys.ENTER)
                            sleep(2)
                            Vk.get_frame(self)
                            sleep(40)
                            self.dwait(2)
                            if not self.ifis_no_exception('//*[contains(text(), "Начать работу")]') and not self.ifis_no_exception(
                                    '//button[contains(text(), "Разрешить")]'):
                                self.dwait(120)
                                if self.ifis_no_exception('//*[contains(text(), "Добро пожаловать")]') \
                                        or self.ifis_no_exception('//*[contains(text(), "Приветствуем")]') \
                                        or self.ifis_no_exception('//*[contains(text(), "Создать тему")]') == True:
                                    self.addcom('ok админка приложения')
                                    break
                                else:
                                    if i == cycle_count_limit:
                                        self.pars_err(
                                            f'fail не увидел "Приветствуем" или "Добро пожаловать" или "Создать тему", после "Начать работу", {i} попыток по {self.t_check} секунд')
                                        break
                                self.dwait(self.wait)
                            else:
                                if i == cycle_count_limit:
                                    self.pars_err(
                                        f'fail после нажатия на Разрешить браузер снова показывал Разрешить, илиНачать работу, {i} попыток по {self.t_check} секунд')
                                    break

                        else:
                            if i == cycle_count_limit:
                                self.pars_err(
                                    f"Скрипт не дождался кнопки \"Начать работу\" спустя {i} попыток по {self.wait} сек")
                                break
                            sleep(10)
                            i += 1
                            driver.refresh()
                            sleep(1)
                            Vk.get_frame(self)

                    if int(datetime.datetime.now().day) / 5 == 0:
                        self.driver.get('https://vk.com/groups')
                        self.dwait(3)
                        for i in range(7):
                            driver.refresh()
                            with suppress(Exception):
                                self.find('//div[(@class="groups_actions_icons")]').click()
                                sleep(1)
                                self.find('//div[(@class="groups_actions_icons")]').click()
                                sleep(1)
                                self.find('//*[contains(text(), "Отписаться")]').click()
                                sleep(1)
                                if self.ifis_no_exception('//*[contains(text(), "Выйти из")]'):
                                    self.find('//*[contains(text(), "Выйти из")]').click()

                except Exception as e:
                    self.pars_err(f"fail ошибка выполнения скрипта, {e}")

                try:
                    self.inter_result[
                        'comment'] += f"\n\n**Описание**________ скрипт создает сообщество, добавляет в него приложение"
                except Exception as e:
                    self.pars_err(f"fail ошибка добавления описания теста в словарь, {e}")

                self.no_sms = True

                if paused == False:
                    pass
                else:
                    test_duration_time = abs(round((test_start_time - datetime.datetime.now()).total_seconds()))
                    if test_duration_time < self.t_check:
                        sleep(self.t_check - test_duration_time)

                self.test_ending()

                if self.inter_result['result'] == 0:
                    return "ok"
                else:
                    return f'fail, {self.inter_result["error"]}'




if __name__ == '__main__':
    for i in range(1):
        print("started at ", time.strftime('%H:%M:%S').replace("'", ""))
        try:
            test_obj = Add_app().test()
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")



