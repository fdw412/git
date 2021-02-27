# -*- coding: utf-8 -*-
import datetime
from gmun_tests.settings import  user_id, app_id_dev, app_id_prod
from gmun_tests import GmunTest
from gmun_tests.utils.vk import Vk
from gmun_tests.utils.mattermost import Mattermost
from time import sleep
import time
import random
from gmun_tests.settings.test_run_params import test_run_params
from gmun_tests.settings import TOKEN_USER



token = "e67978b55a678463bea53426bdf93c382c1b286b8f74f6abfd01eebf15454d784b0abef2eb2d3bc31f602"
uid=user_id


no_driver = False
silent = False

class Ale_Msg_Delayd(GmunTest):
    def __init__(self):
        self.name = 'Ale_Msg_Delayd'
        self.t_check = test_run_params[f'{self.name}']['t_check']
        self.run_series_count = test_run_params[f'{self.name}']['run_series_count']
        self.fail_limit_count = test_run_params[f'{self.name}']['fail_limit_count']
        self.mattermost = Mattermost()
        self.wait = 20
        GmunTest.__init__(self, no_driver, name=self.name)
        self.silent = silent or False

    def test(self, paused=True, dev=False):

        self.dev = dev
        if not dev:
            self.app_id = app_id_prod
            topic_id = 623809
            scenario = 51761
            gid = 190273847
        else:
            self.app_id = app_id_dev
            topic_id = 193
            scenario = 102
            gid = 200162336

        test_start_time = datetime.datetime.now()
        driver = self.driver
        driver.set_page_load_timeout(30)
        self.dwait(self.wait)

        try:
            if Vk.check_unsubscription(self, gid, uid, topic_id, fast=True) != True:
                Vk.unsubscribe(self, gid=gid, uid=uid, topic_id=topic_id)
                sleep(30)

            Vk.vk_login(self, self.wait)
            Vk.check_unsubscription(self, gid, uid, topic_id)

            if self.inter_result["result"] != 1:
                id = random.randint(1, 1000000)
                message = f"новый цикл {time.strftime('%H:%M:%S')}, message {id}"
                Vk.send_to_vk_by_user_request(self, peer_id=-gid, token=TOKEN_USER, message=message)
                Vk.check_delivery(self, msg=id, gid=gid, t_check=self.t_check)

                self.supress_wait_8_sec(driver.get(f"https://vk.com/app{self.app_id}_-{gid}#{topic_id}"))
                Vk.check_subscription(self, gid, uid, topic_id)

                sleep(5)
                ################################################определение времени последнего сообщения со стороны сообщества
                self.dwait(self.wait)
                # Vk.check_last_dialog_msg(self, gid=gid, t_check=self.t_check)
                Vk.check_last_dialog_msg_request(self, gid=gid, token=token)

            Vk.msg_deny(self, gid)

        except Exception as e:
            self.pars_err(f"fail ошибка выполнения скрипта, {e}")


        try:
            self.inter_result['comment'] += f"\n\nОписание________ gid {gid}, скрипт запрещает сообщения запросом в mp.gmun.pro, или vkmul.dev, " \
                                            f"проверяет отсутствие uid в теме запросом к gmun.pro, " \
                                            f"подписывается на тему https://vk.com/app{self.app_id}_-{gid}#{topic_id} " \
                                            f"ожидает появление сообщения в диалог от сценария {scenario}, {self.t_check} секунд"
        except Exception as e:
            self.pars_err(f"fail ошибка добавления описания теста в словарь, {e}")

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




from celery import Celery
from gmun_tests.settings.celery import CELERY_BROKER_URL
app = Celery('gmun_tests', broker=CELERY_BROKER_URL)
from celery.exceptions import SoftTimeLimitExceeded
from gmun_tests.utils.mattermost import Mattermost

@app.task(soft_time_limit=370, time_limit=380, name='ale_msg_delayed')
def ale_msg_delayed():
    try:
        Ale_Msg_Delayd().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"ale_msg_delayed, {e}")

app.control.purge()
app.conf.beat_schedule = {'ale_msg_delayed': {'task': 'ale_msg_delayed','schedule': 420, 'options': {'queue': 'amd'}}}


if __name__ == '__main__':
    for i in range(1):
        print("started at ", time.strftime('%H:%M:%S').replace("'", ""))
        try:
            test_obj = Ale_Msg_Delayd().test(paused=True, dev=False)
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")


