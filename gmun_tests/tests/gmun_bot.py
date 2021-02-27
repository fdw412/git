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

gid = 156229286
uid=585675

no_driver = False
silent = False

class Gmun_Bot(GmunTest):
    def __init__(self):
        self.name = 'Gmun_Bot'
        self.t_check = test_run_params[f'{self.name}']['t_check']
        self.run_series_count = test_run_params[f'{self.name}']['run_series_count']
        self.fail_limit_count = test_run_params[f'{self.name}']['fail_limit_count']
        self.mattermost = Mattermost()
        self.wait = 20
        GmunTest.__init__(self, no_driver, name=self.name)
        self.silent = silent or False


    def test(self, paused=True):
        driver = self.driver
        driver.set_page_load_timeout(30)
        self.dwait(self.wait)

        try:
            test_start_time = datetime.datetime.now()
            Vk.vk_login(self, self.wait)
            msg = f"1 {random.randint(1, 1000000)}"

            self.supress_wait_8_sec(driver.get("https://vk.com/club156229286"))
            sleep(1)
            self.find("//*[text()='Написать сообщение']").click()
            self.find("//*[@id='mail_box_editable']").clear()
            self.find("//*[@id='mail_box_editable']").send_keys(msg)
            self.if_click("//*[text()='Отправить']", "ok отправка сообщения боту в диалог", "fail  отправка сообщения боту в диалог")
            Vk.check_delivery(self, msg=msg, gid=gid, t_check=self.t_check)

        except Exception as e:
            self.pars_err(f"fail ошибка выполнения скрипта, {e}")

        try:
            self.inter_result[
            'comment'] += f"\nОписание________ gid {gid}, скрипт отправляет сообщение боту в диалог и ждет ответа максимум {self.t_check} секунд"
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
            test_obj = Gmun_Bot().test()
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")
