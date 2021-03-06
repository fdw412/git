# -*- coding: utf-8 -*-
import datetime
from gmun_tests.settings import logger
from gmun_tests.settings import TOKEN_USER
from gmun_tests.settings import token_triggers_gid_184517188 as token
from gmun_tests import GmunTest
from gmun_tests.utils.vk import Vk
from gmun_tests.utils.mattermost import Mattermost
from time import sleep
from contextlib import suppress
import time
import random
from gmun_tests.settings.test_run_params import test_run_params
from selenium.webdriver.common.keys import Keys


gid = 184517188
uid=585675
topic_id = 553479

no_driver = False
silent = False


class Triggers_Msg_Dialog(GmunTest):
    def __init__(self):
        self.name = 'Triggers_Msg_Dialog'
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

                if Vk.check_unsubscription(self, gid, uid, topic_id, fast = True) != True:
                    Vk.unsubscribe(self, gid, uid, topic_id, token)
                    sleep(30)

                Vk.vk_login(self, self.wait)
                id = random.randint(1, 1000000)
                message = f"новый цикл {time.strftime('%H:%M:%S')}, message {id}"
                Vk.send_to_vk_by_user_request(self, peer_id=-gid, token=TOKEN_USER, message=message)
                Vk.check_delivery(self, msg=id, gid=gid, t_check=self.t_check)
                Vk.check_unsubscription(self, gid, uid, topic_id)
                Vk.subscribe_by_driver(self, gid, topic_id)
                datetime1 = datetime.datetime.now()
                Vk.check_subscription(self, gid, uid, topic_id)
                delta = int(round((datetime1 - datetime.datetime.now()).total_seconds()))

                if 30-delta > 1:
                    sleep(30-delta)
                message = 1
                Vk.send_to_vk_by_user_request(self, peer_id=-gid, token=TOKEN_USER, message=message)

                if self.inter_result["result"] != 1:
                    try:
                        with suppress(Exception):
                            self.driver.get(f"https://vk.com/im?sel=-{gid}")
                        sleep(1)
                        datetime1 = datetime.datetime.now()
                        for i in range(3+round(self.t_check/10)):
                            self.driver.refresh()
                            self.dwait(1)
                            with suppress(Exception):
                                self.find(".// *[contains(text(), 'Перейти в конец истории')]").click()
                            sleep(1)

                            self.dwait(2)
                            temp = str()
                            delta = abs(round((datetime1 - datetime.datetime.now()).total_seconds()))

                            if self.ifis_no_exception(f".//div[contains(text(), '{id}')]"
                                         f"/following::div[contains(text(), 'блок триггера')]") == True:
                                temp = temp + 'ok сообщение от блока с триггером пришло, '
                            else:
                                temp = temp + f'fail, сообщение от блока с триггером не дождался за {delta} сек., '

                            if self.ifis_no_exception(f".//div[contains(text(), '{id}')]"
                                                            f"/following::div[contains(text(), '1 пришло')]") == True:
                                temp = temp + 'ok триггер сработал, '
                            else:
                                temp = temp + f'fail сообщение сработавшего триггера не дождался за {delta} сек., '

                            if self.ifis_no_exception(f".//div[contains(text(), '{id}')]"
                                                            f"/following::div[contains(text(), '2 не пришло')]") == True:
                                temp = temp + 'ok проверка fallback, '
                            else:
                                temp = temp + f'fail сообщение fallback не дождался за  за {delta} сек., '

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

                Vk.unsubscribe(self, gid, uid, topic_id, token)

            except Exception as e:
                self.pars_err(f"fail ошибка выполнения скрипта, {e}", noscreen=True)

            try:
                self.inter_result['comment'] += f"\n\nОписание________ gid {gid}, сценарий 52845, скрипт отписывается запросом от темы " \
                                            f"{topic_id}, проверяет факт отписки через gmun api, " \
                                            f"отправляет сообщение с random id {id} в диалог с сообществом, " \
                                            f"проверяет его доставку, подписывается на тему {topic_id} в сообществе " \
                                            f"{gid}, ожидает сообщение от первого блока триггера, отправляет ответное " \
                                            f"сообщение, ждет сообщение сработавшего триггера и сообщение от другого триггера, " \
                                            f"который должен отправить fallback сообщение, максимальное ожидание {self.t_check}"
            except Exception as e:
                self.pars_err(f"fail ошибка добавления описания теста в словарь, {e}")

            self.no_sms = False
            if paused == False:
                pass
            else:
                test_duration_time = abs(round((test_start_time - datetime.datetime.now()).total_seconds()))
                if test_duration_time < self.t_check:
                    sleep(self.t_check + 120 - test_duration_time)

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

@app.task(soft_time_limit=400, time_limit=410, name='triggers')
def triggers():
    try:
        Triggers_Msg_Dialog().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"triggers, {e}")

app.control.purge()
app.conf.beat_schedule = {'triggers': {'task': 'triggers','schedule': 420, 'options': {'queue': 'triggers'}}}

if __name__ == '__main__':
        print("started at ", time.strftime('%H:%M:%S').replace("'", ""))
        try:
            test_obj = Triggers_Msg_Dialog().test()
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")


