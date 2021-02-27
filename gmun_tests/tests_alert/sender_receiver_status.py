# -*- coding: utf-8 -*-
import datetime, requests
from gmun_tests.settings import user_id, app_id_prod
from gmun_tests import GmunTest
from gmun_tests.utils.vk import Vk
from gmun_tests.utils.mattermost import Mattermost
from contextlib import suppress
from time import sleep
import time
from gmun_tests.settings.test_run_params import test_run_params
from selenium.webdriver.common.by import By



no_driver = False
silent = False
gid = 201305254
uid = 585675


class Sender_Receiver_Status(GmunTest):
    def __init__(self):
        self.name = 'Sender_Receiver_Status'
        self.t_check = test_run_params[f'{self.name}']['t_check']
        self.run_series_count = test_run_params[f'{self.name}']['run_series_count']
        self.fail_limit_count = test_run_params[f'{self.name}']['fail_limit_count']
        self.mattermost = Mattermost()
        self.wait = 20
        GmunTest.__init__(self, no_driver=True, name=self.name)
        self.silent = silent or False

    def test(self, paused=False):
        try:
            test_start_time = datetime.datetime.now()
            id = self.random_id
            msg = f"{time.strftime('%H:%M:%S')}, Sender_Receiver_Status test {id}"
            url = "https://sender.antipsy.ru/mailing/"
            json = {"vk_group_id": gid, "vk_user_ids": [uid], "message": f"{msg}"}

            headers = {
                'Authorization': 'Token eda373fb132e90b3e2e207664678a1114ed7be21',
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, json=json,)

            if response.status_code == 200:
                pass
            else:
                alert = True
                self.pars_err(f"отправка рассылки для сообщества "
                              f"{gid}: status code {response.status_code}", noscreen=True)

                if type(response.json()) == int:
                    mid = response.json()
                else:
                     self.pars_err(f"отправка рассылки для сообщества "
                                   f"{gid}, в ответе отсутствует mid\n{response.status_code}", noscreen=True)

        except Exception as e:
            self.pars_err(f"отправка рассылки для сообщества {gid}\n{e}`", noscreen=True)


        try:
            self.inter_result[
            'comment'] += f"\n\nОписание________ gid {gid}, скрипт отправляет сообщение по API в sender и проверяет ответ сервиса, " \
                          f"в нем должны быть status_code 200 и mailing_id"
        except Exception as e:
            self.pars_err(f"fail ошибка добавления описания теста в словарь, {e}", noscreen=True)

        if paused == False:
            pass
        else:
            test_duration_time = abs(round((test_start_time - datetime.datetime.now()).total_seconds()))
            if test_duration_time < self.t_check:
                sleep(self.t_check - test_duration_time)

        for i in self.inter_result:
            print(i, self.inter_result[i])

        self.test_ending()


from celery import Celery
from gmun_tests.settings.celery import CELERY_BROKER_URL
app = Celery('gmun_tests', broker=CELERY_BROKER_URL)
from celery.exceptions import SoftTimeLimitExceeded
from gmun_tests.utils.mattermost import Mattermost


@app.task(soft_time_limit=180, time_limit=180, name='sender_receiver_status')
def sender_receiver_status():
    try:
        Sender_Receiver_Status().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"sender_receiver_status, {e}")

with suppress(Exception):
    app.control.purge()
app.conf.beat_schedule = {'sender_receiver_status': {'task': 'sender_receiver_status','schedule': 120, 'options': {'queue': 'sender_receiver_status'}}}

# if __name__ == '__main__':
#     sender_back.apply_async()

if __name__ == '__main__':
    for i in range(1):
        print("started at ", time.strftime('%H:%M:%S').replace("'", ""))
        try:
            test_obj = Sender_Receiver_Status().test(paused=False)
            sleep(0.1)
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")

# if __name__ == '__main__':
#     GmunTest().init_webdriver()


