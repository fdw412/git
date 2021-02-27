# -*- coding: utf-8 -*-
import datetime
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


gid = 191948868
uid=585675
topic_id = 648886
token = '559442ea9a0be70b14cb892239a927ab2db2b9ba7a195ea4067b691ada9fac30f2f4787eb3c43f8571e64'
no_driver = False

first_block_time_limit = 90
second_block_time_limit = 120

silent = False


class Ms_chain_link_follow_check(GmunTest):
    def __init__(self):
        self.name = 'Ms_chain_link_follow_check'
        self.t_check = test_run_params[f'{self.name}']['t_check']
        self.run_series_count = test_run_params[f'{self.name}']['run_series_count']
        self.fail_limit_count = test_run_params[f'{self.name}']['fail_limit_count']
        self.mattermost = Mattermost()
        self.wait = 20
        GmunTest.__init__(self, no_driver, name=self.name)
        self.silent = silent or False

    def test(self, paused=True):
            try:
                test_start_time = datetime.datetime.now()
                driver = self.driver
                driver.set_page_load_timeout(30)
                driver.implicitly_wait(self.wait)

                if Vk.check_unsubscription(self, gid, uid, topic_id, fast=True) != True:
                    Vk.unsubscribe(self, gid, uid, topic_id, token)
                    sleep(30)

                Vk.vk_login(self, self.wait)
                id = random.randint(1, 1000000)
                message = f"новый цикл {time.strftime('%H:%M:%S')}, message {id}"
                Vk.send_to_vk_by_user_request(self, peer_id=-gid, token=TOKEN_USER, message=message)
                Vk.check_delivery(self, msg=id, gid=gid, t_check=self.t_check)
                Vk.check_unsubscription(self, gid, uid, topic_id, long=True)
                Vk.subscribe_by_driver(self, gid, topic_id)
                Vk.check_subscription(self, gid, uid, topic_id)

                # проверка прихода ссылки
                if self.inter_result["result"] != 1:
                    try:
                        with suppress(Exception):
                            self.driver.get(f"https://vk.com/im?sel=-{gid}")
                        sleep(1)
                        datetime1 = datetime.datetime.now()

                        for i in range(round(first_block_time_limit/10)+3):
                            self.driver.refresh()

                            self.dwait(1)
                            with suppress(Exception):
                                self.find(".// *[contains(text(), 'Перейти в конец истории')]").click()
                            sleep(1)

                            self.dwait(2)
                            temp = str()
                            delta = abs(round((datetime1 - datetime.datetime.now()).total_seconds()))

                            if self.ifis_no_exception(f".//div[contains(text(), '{id}')]/following::a[contains(text(), 'https://gmun.pro/go/')]") == True:
                                temp = "ok ссылка пришла, "
                                href = str()
                                href = self.find(f".//div[contains(text(), '{id}')]/following::a[contains(text(), "
                                                 f"'https://gmun.pro/go/')]").get_attribute('href')
                                sleep(1)
                                self.driver.get(href)
                            else:
                                temp = f"fail ссылка не пришла за {delta} сек., "

                            if temp.find("fail") == -1:
                                self.addcom(f"{temp}")
                                break
                            else:
                                sleep(10)
                                if abs(round((datetime1 - datetime.datetime.now()).total_seconds())) >= first_block_time_limit:
                                    self.dwait(self.wait)
                                    self.pars_err(temp)
                                    break

                    except Exception as e:
                        self.pars_err(f"fail ошибка при проверке прихода ссылки, {e}")



                limit = 100
                if limit - delta > 2:
                    sleep(limit-delta)
                else:
                    self.pars_err(f"Время на подписку и проверку прихода первого сообщения, заняло {limit} сек, "
                                  "это больше чем позволяет макисмальный интервал для корректного прохождения "
                                  "теста, состоящего из более двух сообщений")



                # проверка прихода сообщения после проверки перехода по ссылке
                if self.inter_result["result"] != 1:
                    try:
                        with suppress(Exception):
                            self.driver.get(f"https://vk.com/im?sel=-{gid}")
                        sleep(1)
                        datetime1 = datetime.datetime.now()

                        for i in range(round(second_block_time_limit/10)+3):
                            self.driver.refresh()

                            self.dwait(1)
                            with suppress(Exception):
                                self.find(".// *[contains(text(), 'Перейти в конец истории')]").click()
                            sleep(1)

                            self.dwait(2)
                            temp = str()
                            delta = abs(round((datetime1 - datetime.datetime.now()).total_seconds()))

                            if self.ifis_no_exception(f".//div[contains(text(), '{id}')]/following::div[contains(text(), 'переход да')]") == True:
                                temp = "ok переход по ссылке засчитан, "
                            else:
                                temp = f"fail правильный ответ блока проверки перехода не обнаружен в течении {delta} сек., "

                            if temp.find("fail") == -1:
                                self.addcom(f"{temp}")
                                break
                            else:
                                sleep(10)
                                if abs(round((datetime1 - datetime.datetime.now()).total_seconds())) >= second_block_time_limit:
                                    self.dwait(self.wait)
                                    self.pars_err(temp)
                                    break

                    except Exception as e:
                        self.pars_err(f"fail ошибка при проверке ответа блока перехода по ссылке, {e}")



                Vk.unsubscribe(self, gid, uid, topic_id, token)
            except Exception as e:
                self.pars_err(f"fail ошибка выполнения скрипта, {e}")

            try:
                self.inter_result['comment'] += f"\nОписание________ gid {gid}, скрипт отписывается запросом от темы " \
                                            f"{topic_id}, проверяет факт отписки через gmun api, " \
                                            f"отправляет сообщение с random id {id} в диалог с сообществом, " \
                                            f"проверяет его доставку, подписывается на тему {topic_id} в сообществе " \
                                            f"{gid}, проверяет в диалоге доставку сообщения от первого блока со ссылкой в течении max {first_block_time_limit} секунд, переходит по ссылке" \
                                                f" в диалоге, и спустя {limit} секунд начинает проверять доставку сообщения от блока валидной проверки перехада в течении" \
                                                f" max {second_block_time_limit} секунд"
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
            test_obj = Ms_chain_link_follow_check().test()
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")


