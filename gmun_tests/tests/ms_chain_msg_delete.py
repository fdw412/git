# -*- coding: utf-8 -*-
import datetime
from gmun_tests.settings import logger
from gmun_tests import GmunTest
from gmun_tests.utils.vk import Vk
from gmun_tests.utils.mattermost import Mattermost
from time import sleep
import time
import random
from gmun_tests.settings.test_run_params import test_run_params
from gmun_tests.settings import TOKEN_USER
from contextlib import suppress




gid = 183846381
uid=585675
topic_id = 687353
scenario = 59645

no_driver = False
silent = False

class Ms_Chain_Msg_Delete(GmunTest):
    def __init__(self):
        self.name = 'Ms_Chain_Msg_Delete'
        self.t_check = test_run_params[f'{self.name}']['t_check']
        self.run_series_count = test_run_params[f'{self.name}']['run_series_count']
        self.fail_limit_count = test_run_params[f'{self.name}']['fail_limit_count']
        self.mattermost = Mattermost()
        self.wait = 20
        GmunTest.__init__(self, no_driver, name=self.name)
        self.silent = silent or False

    def test(self, paused=True):
        test_start_time = datetime.datetime.now()
        driver = self.driver
        driver.set_page_load_timeout(30)
        self.dwait(self.wait)

        try:
            if Vk.check_unsubscription(self, gid, uid, topic_id, fast=True) != True:
                Vk.msg_deny(self, gid)
                sleep(30)

            Vk.vk_login(self, self.wait)
            Vk.check_unsubscription(self, gid, uid, topic_id, long=True)

            id = random.randint(1, 1000000)
            message = f"новый цикл {time.strftime('%H:%M:%S')}, message {id}"
            Vk.send_to_vk_by_user_request(self, peer_id=-gid, token=TOKEN_USER, message=message)
            Vk.check_delivery(self, msg=id, gid=gid, t_check=self.t_check)
            Vk.subscribe_by_driver(self, gid, topic_id)
            Vk.check_subscription(self, gid, uid, topic_id)
            sleep(70)
            if self.inter_result["result"] != 1:
                try:
                    with suppress(Exception):
                        self.driver.get(f"https://vk.com/im?sel=-{gid}")
                    sleep(1)
                    datetime1 = datetime.datetime.now()
                    for i in range(round(self.t_check / 10) + 3):
                        self.driver.refresh()

                        self.dwait(1)
                        with suppress(Exception):
                            self.find(".// *[contains(text(), 'Перейти в конец истории')]").click()
                        sleep(1)

                        self.dwait(2)
                        temp = str()
                        delta = int(round((datetime1 - datetime.datetime.now()).total_seconds()))

                        if self.ifis_no_exception(f".//div[contains(text(), '{id}')]"
                                     f"/following::div[contains(text(), 'первое')]") == True:
                            temp = "ok первое сообщение пришло, "
                        else:
                            temp = f"fail первое сообщение не пришло, ожидание {abs(delta)} сек., "

                        if not self.ifis_no_exception(f".//div[contains(text(), '{id}')]"
                                     f"/following::div[contains(text(), 'второе')]") == True:
                            temp = "ok второе сообщение удалилось, "
                        else:
                            temp = f"fail второе сообщение не удалилось, ожидание {abs(delta)} сек., "

                        if temp.find("fail") == -1:
                            self.addcom(f"{temp}")
                            break
                        else:
                            sleep(10)
                            if abs(round((datetime1 - datetime.datetime.now()).total_seconds())) >= self.t_check:
                                self.dwait(self.wait)
                                self.pars_err(temp)
                                break
                except Exception as e:
                    self.pars_err(f"fail ошибка при проверке сообщений от сценария, {e}")

                Vk.msg_deny(self, gid)

        except Exception as e:
            self.pars_err(f"fail ошибка выполнения скрипта, {e}")


        try:
            self.inter_result['comment'] += f"\n\nОписание________ gid {gid}, скрипт запрещает сообщения запросом в mp.gmun.pro, " \
                                            f"подписывается на тему https://vk.com/app5728966_-{gid}#{topic_id} " \
                                            f"ожидает появление первого сообщения в диалог от сценария {scenario}, ждет 70 секунд, " \
                                            f"и начинает проверять успешность удаления сообщения второго блока в течении {self.t_check} секунд"
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
            test_obj = Ms_Chain_Msg_Delete().test()
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")


