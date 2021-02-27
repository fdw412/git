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


gid = 192529621
uid=585675
topic_id = 649602
token = token_ms_chain_2020_gid_191083897
no_driver = False

first_block_time_limit = 90
second_block_time_limit = 120

silent = False

class Ms_chain_action_read_check_positive(GmunTest):
    def __init__(self):
        self.name = 'Ms_chain_action_read_check_positive'
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
                datetime1 = datetime.datetime.now()
                Vk.check_subscription(self, gid, uid, topic_id)

                # проверка прихода первого сообщения

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

                            if self.ifis_no_exception(f".//div[contains(text(), '{id}')]"
                                                  f"/following::div[contains(text(), 'сообщение прочитано да 1')]") == True:
                                temp = "ok первое сообщение пришло, "
                            else:
                                temp = f"fail первое сообщение не пришло за {delta} сек., "

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
                        self.pars_err(f"fail ошибка при проверке сообщений от сценария, {e}")

                    limit = 100
                    if limit - delta < 5:
                        self.pars_err(f"Время на подписку и проверку, заняло {limit} сек, "
                                      "это больше чем позволяет макисмальный интервал для корректного прохождения "
                                      "теста, состоящего из более двух сообщений")

                    if self.inter_result["result"] != 1:
                        try:
                            with suppress(Exception):
                                self.driver.get(f"https://vk.com/im?sel=-{gid}")
                            sleep(1)
                            datetime1 = datetime.datetime.now()

                            for i in range(int(self.t_check / 10)):
                                self.driver.refresh()

                                self.dwait(1)
                                with suppress(Exception):
                                    self.find(".// *[contains(text(), 'Перейти в конец истории')]").click()
                                sleep(1)

                                self.dwait(2)
                                temp = str()
                                delta = abs(round((datetime1 - datetime.datetime.now()).total_seconds()))

                                if self.ifis_no_exception(f".//div[contains(text(), '{id}')]"
                                             f"/following::div[contains(text(), 'сообщение прочитано да 2')]") == True:
                                    temp = "ok второе сообщение пришло "
                                else:
                                    temp = f"fail второе сообщение не пришло за {delta} сек.,  "

                                if temp.find("fail") == -1:
                                    self.addcom(f"{temp}")
                                    break
                                else:
                                    sleep(10)
                                    if abs(round((
                                                         datetime1 - datetime.datetime.now()).total_seconds())) >= second_block_time_limit or i == round(
                                            second_block_time_limit / 10):
                                        self.dwait(self.wait)
                                        self.pars_err(temp)
                                        break

                        except Exception as e:
                            self.pars_err(f"fail ошибка при проверке сообщений от сценария, {e}")

                Vk.unsubscribe(self, gid, uid, topic_id, token)
            except Exception as e:
                self.pars_err(f"fail ошибка выполнения скрипта, {e}")

            try:
                self.inter_result['comment'] += f"\nОписание________ gid {gid}, сценарий 53588, скрипт отписывается запросом от темы " \
                                            f"{topic_id}, проверяет факт отписки через gmun api, " \
                                            f"отправляет сообщение с random id {id} в диалог с сообществом, " \
                                            f"проверяет его доставку, подписывается на тему {topic_id} в сообществе " \
                                            f"{gid}, проверяет в диалоге доставку сообщения от первого блока, отмечается в диалоге, " \
                                                f"чтобы сообщение было прочитано и спустя минуту начинает проверять доставку сообщения от блока валидной " \
                                                f"проверки прочтения сообщения, максимальное ожидание {self.t_check}"
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
                return "test ok"
            else:
                return f'test fail, {self.inter_result["error"]}'


if __name__ == '__main__':
    for i in range(1):
        print("started at ", time.strftime('%H:%M:%S').replace("'", ""))
        try:
            test_obj = Ms_chain_action_read_check_positive().test()
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")


