# -*- coding: utf-8 -*-
import datetime
from gmun_tests.settings import logger
from gmun_tests.settings import TOKEN_USER
from gmun_tests import GmunTest
from gmun_tests.settings import token_ms_chain_2020_gid_191083897
from gmun_tests.utils.vk import Vk
from gmun_tests.utils.mattermost import Mattermost
from time import sleep
from contextlib import suppress
import time
import random
import requests
from gmun_tests.settings.test_run_params import test_run_params
from selenium.webdriver.common.keys import Keys


gid = 191083897
uid=585675
topic_id1 = 633364
topic_id2 = 633646
token = token_ms_chain_2020_gid_191083897

no_driver = False
silent = False


class Ms_Chain_Action_Subscr_Unsubscr(GmunTest):
    def __init__(self):
        self.name = 'Ms_Chain_Action_Subscr_Unsubscr'
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

                for i in range(2):
                    if Vk.check_unsubscription(self, gid, uid, topic_id1, fast=True) \
                            and Vk.check_unsubscription(self, gid, uid, topic_id2, fast=True)!= True:
                        Vk.unsubscribe(self, gid, uid, topic_id1, token)
                        Vk.unsubscribe(self, gid, uid, topic_id2, token)
                        sleep(20)
                    else:
                        break

                Vk.check_unsubscription(self, gid, uid, topic_id1, long=True)
                Vk.check_unsubscription(self, gid, uid, topic_id2, long=True)

                timeout = 90
                if self.inter_result["result"] != 1:
                    Vk.vk_login(self, self.wait)
                    self.supress_wait_8_sec(driver.get(f"https://vk.com/app5728966_-{gid}#{topic_id1}"))
                    Vk.check_subscription(self, gid, uid, topic_id1)
                    sleep(timeout)
                    if self.inter_result["result"] != 1:
                        if Vk.check_subscription(self, gid, uid, topic_id2) == True:
                            self.addcom("ok действие подписки на тему")
                        else:
                            self.pars_err("fail действие подписки на тему")

                    if self.inter_result["result"] != 1:
                        if Vk.check_unsubscription(self, gid, uid, topic_id1) == True:
                            self.addcom("ok действие отписки от темы")
                        else:
                            self.pars_err("fail действие действие отписки от темы")

                with suppress(Exception):
                    url = "https://interlayer-subscription.antipsy.ru/unsubscribe/?sign=-oC66ed37Ksz9b8pe8f7SbtJGzGVj5M1F7avZzNXIbA&v=2.1&vk_access_token_settings=&vk_app_id=5728966&vk_are_notifications_enabled=0&vk_group_id=191083897&vk_is_app_user=1&vk_is_favorite=0&vk_language=ru&vk_platform=desktop_web&vk_ref=other&vk_ts=1611595180&vk_user_id=585675&vk_viewer_group_role=admin"

                    payload = "{\"group_id\":\"191083897\",\"user_id\":\"585675\",\"theme_id\":633364}"
                    headers = {
                        'authorization': 'Bearer n3zpeuWpJBeGhoirspssI0znGjUFwIuD',
                        'Content-Type': 'application/json'
                    }
                    response = requests.request("POST", url, headers=headers, data=payload)


                Vk.unsubscribe(self, gid, uid, topic_id1, token)
                Vk.unsubscribe(self, gid, uid, topic_id2, token)

            except Exception as e:
                self.pars_err(f"fail ошибка выполнения скрипта, {e}")

            try:
                self.inter_result['comment'] += f"\nОписание________ gid {gid}, скрипт отписывается запросом от тем, " \
                                            f"проверяет факт отписки через gmun api, подписывается на тему {topic_id1}, " \
                                            f"ждет {timeout} секунд, проверяет подписку на тему {topic_id2}, и отписку от темы {topic_id1}"
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
            test_obj = Ms_Chain_Action_Subscr_Unsubscr().test()
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")


