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
silent = False


class Interface(GmunTest):
    def __init__(self):
        self.name = 'Interface'
        self.t_check = test_run_params[f'{self.name}']['t_check']
        self.run_series_count = test_run_params[f'{self.name}']['run_series_count']
        self.fail_limit_count = test_run_params[f'{self.name}']['fail_limit_count']
        self.mattermost = Mattermost()
        self.wait = 30
        GmunTest.__init__(self, no_driver, name=self.name)
        self.silent = silent or False

    def test(self, paused=True):
            try:
                test_start_time = datetime.datetime.now()
                driver = self.driver
                driver.set_page_load_timeout(30)
                self.dwait(self.wait)


                Vk.vk_login(self, self.wait)
                id = random.randint(1, 1000000)


                try:
                    # переменные и условия в конструкторе
                    sleep(1)
                    driver.get("https://vk.com/app5728966_-172321382#page_id=8047")
                    sleep(10)
                    Vk.get_frame(self)
                    sleep(1)
                    if self.ifis_no_exception(".//*[contains(text(), 'Владислав_') or contains(text(), 'Vladislav_')]", wait=60):
                        self.addcom("\nok конструктор переменная имени")
                    else:
                        self.pars_err(f"\nfail конструктор переменная имени")
                    self.dwait(1)

                    if self.ifis_no_exception(".//*[contains(text(), '_Мужской_')]"):
                        self.addcom("\nok конструктор условие показа элемента, если пол мужской")
                    else:
                        self.pars_err(f"\nfail конструктор условие показа элемента, если пол мужской")

                    if self.ifis_no_exception(".//*[contains(text(), 'Подписан на Условие подписки_')]"):
                        self.addcom("\nok конструктор условие показа элемента, если подписан на тему")
                    else:
                        self.pars_err(f"\nfail конструктор условие показа элемента, если подписан на тему")

                    self.dwait(self.wait)

                except Exception as e:
                    self.pars_err(f"fail переменные и условия в конструкторе {e}")


                self.dwait(self.wait)
                try:
                    # создание темы ключевого слова и хештега
                    driver.get(f"https://vk.com/app5728966_-{gid}")
                    sleep(1)
                    Vk.get_frame(self)
                    sleep(1)
                    self.find('html').send_keys(Keys.HOME)
                    sleep(1)
                    self.find(".//button[@class='button' and  contains(text(), 'Создать тему')]").click()
                    sleep(1)
                    self.find(".//input[@id='.title']").send_keys(id)
                    sleep(1)
                    self.find(".//div[@class='Select-placeholder']").click()
                    sleep(1)
                    self.find(".//div[@class='Select-placeholder']/../div[2]/input").send_keys(f"tag{id}", Keys.ENTER)
                    sleep(2)
                    self.find(".//input[@id='.keys']").send_keys(f"key{id}", Keys.ENTER)
                    sleep(3)
                    self.find(".//input[@value='Создать']").click()

                    # проверка создания темы
                    sleep(10)
                    driver.refresh()
                    sleep(2)
                    Vk.get_frame(self)
                    self.find('html').send_keys(Keys.HOME)
                    sleep(1)
                    self.find(".//a[@href='/senderman/themes']").click()

                    if self.ifis_no_exception(f".//*[contains(text(), '{id}')]") == True:
                        self.addcom("\nok создание темы")
                    else:
                        self.pars_err("\nfail создание темы")
                except Exception as e:
                    self.pars_err(f"fail создание темы {e}")


                self.dwait(self.wait)
                try:
                    # проверка ключевого слова
                    driver.get(f"https://vk.com/app5728966_-{gid}")
                    sleep(1)
                    Vk.get_frame(self)
                    sleep(1)
                    self.find('html').send_keys(Keys.HOME)
                    sleep(1)
                    i = 1
                    driver.implicitly_wait(7)
                    while i <= 6:
                        i += 1
                        driver.refresh()
                        sleep(2)
                        Vk.get_frame(self)
                        self.find(".//a[@href='/senderman/themes']").click()
                        sleep(1)
                        self.find(f".//header/h3[contains(text(), '{id}')]/../../footer/div[1]/button[2]").click()
                        sleep(2)
                        if self.ifis_no_exception(f".//div[@class='Select-multi-value-wrapper'  and contains(*, 'key{id}')]"):
                            self.addcom('\nok сохранение ключевого слова')
                            break
                        else:
                            if i == 6:
                                self.pars_err('\nfail сохранение ключевого слова')
                            sleep(5)
                    driver.implicitly_wait(self.wait)
                except Exception as e:
                    self.pars_err(f"fail сохранение ключевого слова {e}")


                self.dwait(self.wait)
                try:
                    # проверка хештега
                    driver.get(f"https://vk.com/app5728966_-{gid}")
                    sleep(1)
                    Vk.get_frame(self)
                    sleep(1)
                    self.find('html').send_keys(Keys.HOME)
                    sleep(1)
                    i = 1
                    driver.implicitly_wait(7)
                    while i <= 6:
                        i += 1
                        driver.refresh()
                        sleep(2)
                        Vk.get_frame(self)

                        self.find(".//a[@href='/senderman/themes']").click()
                        sleep(1)
                        self.find(f".//header/h3[contains(text(), '{id}')]/../../footer/div[1]/button[2]").click()
                        sleep(2)
                        if self.ifis_no_exception(f".//div[@class='Select-multi-value-wrapper'  and contains(*, 'tag{id}')]"):
                            self.addcom("\nok сохранение хештега")
                            break
                        else:
                            if i == 6:
                                self.pars_err("\nfail сохранение хештега")
                                break
                            sleep(5)
                    driver.implicitly_wait(self.wait)

                except Exception as e:
                    self.pars_err(f"fail сохранение хештега {e}")


                self.dwait(self.wait)
                try:
                    # удаление темы
                    driver.get(f"https://vk.com/app5728966_-{gid}")
                    sleep(1)
                    Vk.get_frame(self)
                    sleep(1)
                    self.find('html').send_keys(Keys.HOME)
                    sleep(1)
                    driver.implicitly_wait(10)
                    self.find(".//a[@href='/senderman/themes']").click()
                    self.find(f".//header/h3[contains(text(), '{id}')]/../../footer/div[1]/button[6]").click()
                    sleep(1)
                    with suppress(Exception):
                        driver.switch_to.alert.accept()

                    driver.implicitly_wait(self.wait)
                    sleep(2)

                except Exception as e:
                    self.pars_err(f"fail удаление темы {e}")

                try:
                    # сохранение секрета в настройках
                    driver.get(f"https://vk.com/app5728966_-{gid}")
                    sleep(1)
                    Vk.get_frame(self)
                    sleep(1)
                    self.find('html').send_keys(Keys.HOME)
                    sleep(1)
                    self.find(".//a[@href='/senderman/settings']").click()
                    sleep(1)
                    self.find(".//input[@name='forms.secretKeyForm.secretKey']").send_keys(id)
                    sleep(1)
                    self.find(".//button[contains(text(), 'Добавить')]").click()
                    i = 1
                    driver.implicitly_wait(7)
                    while i <= 6:
                        i += 1
                        driver.refresh()
                        sleep(2)
                        Vk.get_frame(self)
                        self.find(".//a[@href='/senderman/settings']").click()
                        sleep(3)

                        if self.ifis_no_exception(f".//label[contains(text(), '{id}')]") == True:
                            self.addcom("\nok сохранение секрета paymaster")
                            break
                        else:
                            if i == 6:
                                self.pars_err("\nfail сохранение секрета paymaster")

                            sleep(5)
                    driver.implicitly_wait(self.wait)
                    self.dwait(5)
                    for i in range(2):
                        if self.ifis_no_exception(".//button[@class='form-button secret-key-form-button']") == True:
                            self.find(".//button[@class='form-button secret-key-form-button']").click()
                            sleep(2)
                    self.dwait(5)

                except Exception as e:
                    self.pars_err(f"fail сохранение секрета {e}")

                self.dwait(self.wait)
                try:
                    # загрузка картинки в storage
                    driver.get(f"https://vk.com/app5728966_-{gid}")
                    sleep(1)
                    Vk.get_frame(self)
                    sleep(1)
                    self.find('html').send_keys(Keys.HOME)
                    sleep(1)
                    self.find(".//a[@href='/senderman/constructor']").click()
                    sleep(1)
                    self.find(".//input[@id='.selectedPageId']").send_keys("11111111")
                    sleep(1)
                    self.find(".//input[@id='.selectedPageId']").send_keys(Keys.ENTER)
                    self.find(".//li[@data-tab-id='6']").click()
                    sleep(1)
                    self.find(".//li[@data-tab-id='6']").click()
                    sleep(3)
                    self.find(".//label[contains(text(), 'Фоновое')]/following::input[@type='file']").send_keys(
                        os.sep.join([os.path.dirname(__file__), '__uploader_test.jpg']))
                    slp=10
                    sleep(slp)
                    for i in range(2):
                        self.find(".//button[contains(text(), 'Применить')]").click()
                        sleep(2)
                    if self.ifis_no_exception(".//*[contains(text(), 'uploader_test')]"):
                        self.addcom("\nok сохранение картинки в storage")
                    else:
                        self.pars_err(f"\nfail сохранение картинки в storage, не найден спустя {slp} сек.")

                except Exception as e:
                    self.pars_err(f"fail сохранение картинки в storage {e}")

                try:
                # загрузка картинки в аплоадер
                    driver.get(f"https://vk.com/app5728966_-{gid}")
                    sleep(1)
                    Vk.get_frame(self)
                    sleep(1)
                    self.find('html').send_keys(Keys.HOME)
                    sleep(1)
                    self.find(".//a[@id='btn-mail-link']").click()
                    sleep(3)
                    self.find(".//span[text()='Список ссылок на VK материалы']/parent::button[1]").click()
                    sleep(2)
                    self.driver.find_element_by_xpath(".//input[@data-test-id='uploader-photo']").send_keys(
                        os.sep.join([os.path.dirname(__file__), '__uploader_test.jpg']))
                    sleep(2)
                    if self.ifis_no_exception(".//textarea[@id='.attachments' and contains(text(), 'photo')]"):
                        self.addcom("\nok сохранение картинки в uploader")
                    else:
                        self.pars_err("\nfail сохранение картинки в uploader")

                except Exception as e:
                    self.pars_err(f"fail сохранение картинки в uploader {e}")

                try:
                    # загрузка файла в аплоадер
                    driver.get(f"https://vk.com/app5728966_-{gid}")
                    sleep(1)
                    Vk.get_frame(self)
                    sleep(1)
                    self.find('html').send_keys(Keys.HOME)
                    sleep(1)
                    self.find(".//a[@id='btn-mail-link']").click()
                    sleep(3)
                    self.find(".//span[text()='Список ссылок на VK материалы']/parent::button[1]").click()
                    sleep(1)
                    self.driver.find_element_by_xpath(".//input[@data-test-id='uploader-doc']").send_keys(
                        os.sep.join([os.path.dirname(__file__), '__uploader_test.txt']))
                    sleep(2)
                    if self.ifis_no_exception(".//textarea[@id='.attachments' and contains(text(), 'doc')]"):
                        self.addcom("\nok сохранение файла в uploader")
                    else:
                        self.pars_err("\nfail сохранение файла в uploader")

                except Exception as e:
                    self.pars_err(f"fail сохранение файла в uploader {e}")

                try:
                    # сохранение UTM
                    driver.get(f"https://vk.com/app5728966_-{gid}")
                    sleep(1)
                    Vk.get_frame(self)
                    sleep(1)
                    self.find('html').send_keys(Keys.HOME)
                    sleep(1)
                    self.find(".//a[@href='/senderman/utm']").click()
                    sleep(1)
                    self.find(".//*[contains(text(), 'Создание')]/../button[1]").click()
                    sleep(2)
                    self.find(".//*[@id='.urlName']").clear()
                    sleep(2)
                    utm = random.randint(1, 1000000)
                    self.find(".//*[@id='.urlName']").send_keys(utm)
                    sleep(2)
                    self.find(".//button[contains(text(), 'Сохранить')]").submit()
                    sleep(7)
                    self.find(".//*[contains(text(), 'Сохранённые')]/../button[1]").click()
                    sleep(10)
                    if self.ifis_no_exception(f".//label[contains(text(), '{utm}')]/following::input[1][@value='https://vk.com/app5728966_-{gid}']") == True:
                        self.addcom("\nok сохранение UTM")
                    else:
                        self.pars_err("\nfail  сохранение UTM")

                except Exception as e:
                    self.pars_err(f"fail создание темы {e}")

                try:
                    # получение UTM статистики
                    driver.get(f"https://vk.com/app5728966_-{gid}")
                    sleep(1)
                    Vk.get_frame(self)
                    sleep(1)
                    self.find('html').send_keys(Keys.HOME)
                    sleep(1)
                    self.find(".//a[@href='/senderman/utm']").click()
                    sleep(1)
                    self.find(".//div[@class='utm-unfolder'][3]/header[1]/button[1]").click()
                    sleep(2)
                    self.find('html').send_keys(Keys.PAGE_DOWN)
                    sleep(1)
                    self.find(".//input[@placeholder='С самого начала']").clear()
                    sleep(2)
                    self.find(".//input[@placeholder='С самого начала']").send_keys("18.02.2020 00:00")
                    sleep(2)
                    self.find(".//*[@id='utm-vkuid']").click()
                    sleep(2)
                    self.find(".//button[text()='Получить статистику']").submit()
                    sleep(1)
                    if self.ifis_no_exception(f".//*[contains(text(),'Визит')]") == True:
                        self.addcom("\nok получение UTM статистики")
                    else:
                        self.adderr("\nfail получение UTM статистики")

                except Exception as e:
                    self.pars_err(f"fail получение UTM статистики {e}")


            except Exception as e:
                self.pars_err(f"fail ошибка выполнения скрипта, {e}")

            try:
                self.inter_result['comment'] += f"\nОписание________ gid {gid}, скрипт создает тему, " \
                                                f"ключевое, слово, сохраняет яндекс секрет, сохраняет UTM метку, " \
                                                f"получает UTM статистику, сохраняет картинку в Uploader и др."
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
            test_obj = Interface().test()
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")


