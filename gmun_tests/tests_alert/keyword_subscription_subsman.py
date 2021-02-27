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



gid = 192400503
uid=585675
topic_id = 1336315
token = "a6c9ce20c397243290d1d725d2dc8630da0491e754aa4eebda74e75a1ad4d9b6077a0c19ac03dbc4678bf"

no_driver = False
silent = False

class Keyword_Subscription_Subsman(GmunTest):
    def __init__(self):
        self.name = 'Keyword_Subscription_Subsman'
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

            if Vk.check_unsubscription_subsman(self, gid, uid, topic_id, fast=True) != True:
                Vk.msg_deny(self, gid)
                sleep(30)

            Vk.vk_login(self, self.wait)
            Vk.check_unsubscription_subsman(self, gid, uid, topic_id)

            if self.inter_result["result"] != 1:
                self.supress_wait_8_sec(driver.get(f"https://vk.com/club{gid}"))
                text = "переход по ссылке для отправки сообщения в диалог"
                self.if_click("//div[@class='group_send_msg_status_block_title']", f"ok {text}", f"fail {text}")
                self.find("//div[@id='mail_box_editable']").clear()
                id = random.randint(1000000, 1000000000)
                msg = str(time.strftime('%H:%M:%S').replace("'", "") + f" {id}")
                self.find("//div[@id='mail_box_editable']").send_keys(f"key {msg}")
                self.if_click("//*[@id='mail_box_send']", "ok клик по отправке сообщений в вк", "fail клик по отправке сообщений в вк")
                sleep(5)
                ################################################определение времени последнего сообщения со стороны сообщества
                Vk.check_last_dialog_msg_request(self, gid=gid, token = token)


            Vk.msg_deny(self, gid)

        except Exception as e:
            self.pars_err(f"fail ошибка выполнения скрипта, {e}")

        try:
            self.inter_result['comment'] += f"\n\nОписание________ gid {gid}, скрипт запрещает сообщения запросом в subsman, " \
                                        f"проверяет отсутствие uid в теме запросом к subsman, " \
                                        f"отправляет сообщение в диалог сообщества, " \
                                        f"ожидает появление в диалоге максимум {self.t_check} секунд"
        except Exception as e:
            self.pars_err(f"fail ошибка добавления описания теста в словарь, {e}", noscreen=True)

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
            test_obj = Keyword_Subscription_Subsman().test()
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")
