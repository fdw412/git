# -*- coding: utf-8 -*-
import datetime
from gmun_tests.settings import user_id, app_id_dev, app_id_prod
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
gid = 164179533

class Sender_Front(GmunTest):
    def __init__(self):
        self.name = 'Sender_Front'
        self.t_check = test_run_params[f'{self.name}']['t_check']
        self.run_series_count = test_run_params[f'{self.name}']['run_series_count']
        self.fail_limit_count = test_run_params[f'{self.name}']['fail_limit_count']
        self.mattermost = Mattermost()
        self.wait = 20
        GmunTest.__init__(self, no_driver, name=self.name)
        self.silent = silent or False
    def test(self, paused=True, dev=False):
        try:
            self.dev = dev
            if not dev:
                self.app_id = app_id_prod
            else:
                self.app_id = app_id_dev

            test_start_time = datetime.datetime.now()
            driver = self.driver
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(self.wait)

            # login to vk
            Vk.vk_login(self, self.wait)

            self.supress_wait_8_sec(driver.get(f"https://vk.com/app{self.app_id}_-{gid}"))
            sleep(2)
            Vk.get_frame(self)
            self.if_click(".//a[@id='btn-mail-link']", "загрузка вкладки создания рассылки ok", "загрузка вкладки создания рассылки fail")
            self.if_click(".//div[contains(text(), 'Выберите тему')]", "выбор темы ok", "выбор темы fail")
            self.if_click(".//div[contains(text(), 'autotest_topic_1')]", "выбор темы ok", "выбор темы fail")
            self.if_click(".//textarea[contains(@class, 'sc-')]", "поле ввода сообщения ok", "поле ввода сообщения fail")
            self.find(".//textarea[contains(@class, 'sc-')]").clear()
            id = self.random_id
            if not self.dev:
                msg = f"{time.strftime('%H:%M:%S')}, sender frontend test {id}"
            else:
                msg = f"{time.strftime('%H:%M:%S')}, dev sender frontend test {id}"

            self.find(".//textarea[contains(@class, 'sc-')]").send_keys(msg)
            self.if_click(".//button[contains(text(), 'Запустить')]", "запуск рассылки ok", "запуск рассылки fail")
            sleep(2)
            self.if_click(f".//div[contains(text(), '{msg}')]", "появление отправки в истории ok", "появление отправки в истории fail")
            sleep(10)

            Vk.check_delivery(self, msg=id, gid=gid, t_check=self.t_check)



        except Exception as e:
            self.pars_err(f"fail ошибка выполнения скрипта, {e}")

        try:
            self.inter_result[
            'comment'] += f"\n\nОписание________ gid {gid}, скрипт отправляет сообщение через расыльщик и проверят его наличие в диалоге, " \
                          f"максимальное ожидание {self.t_check} секунд"
        except Exception as e:
            self.pars_err(f"fail ошибка добавления описания теста в словарь, {e}", noscreen=True)

        #
        # self.inter_result = {'result': 0, 'results_line':[], 'results_line_datetime':[], 'error': 'эмулиция ошибки', 'screen_paths':
        #     ['D:\\PycharmProjects\\git\\gmun_tests\\settings\\..\\screenshots\\___none.png',
        #      'D:\\PycharmProjects\\git\\gmun_tests\\settings\\..\\screenshots\\___none.png'],
        #                 'comment': 'эмуляция ошибки'}


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


@app.task(soft_time_limit=320, time_limit=330, name='sender_front')
def sender_front():
    try:
        Sender_Front().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"sender_front, {e}")

with suppress(Exception):
    app.control.purge()
app.conf.beat_schedule = {'sender_front': {'task': 'sender_front','schedule': 300, 'options': {'queue': 'sender_front'}}}

# if __name__ == '__main__':
#     sender_front.apply_async()

if __name__ == '__main__':
    for i in range(1):
        print("started at ", time.strftime('%H:%M:%S').replace("'", ""))
        try:
            test_obj = Sender_Front().test(paused=False, dev=False)
            sleep(0.1)
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")

# if __name__ == '__main__':
#     GmunTest().init_webdriver()


