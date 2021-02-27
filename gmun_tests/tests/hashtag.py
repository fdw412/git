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

gid = 161143917
uid=585675

no_driver = False
silent = False

class Hashtag(GmunTest):
    def __init__(self):
        self.name = 'Hashtag'
        self.t_check = test_run_params[f'{self.name}']['t_check']
        self.run_series_count = test_run_params[f'{self.name}']['run_series_count']
        self.fail_limit_count = test_run_params[f'{self.name}']['fail_limit_count']
        self.mattermost = Mattermost()
        self.wait = 20
        GmunTest.__init__(self, no_driver, name=self.name)
        self.silent = silent or False


    def test(self, paused=True):

            if random.randint(1, 2) == 1:
                gid = 157361022
            else:
                gid = 161143917

            time_delta_minutes = 16
            try:
                self.last_call_get()
                last_call = datetime.datetime.fromtimestamp(int(str(self.last_call).replace("\"", "")))
                now = datetime.datetime.now()
                time_delta_minutes = round(abs((now - last_call).total_seconds() / 60))
            except Exception as e:
                print(e)
                logger.error(e)

            if time_delta_minutes < 16:
                sleep(180)
            else:
                gid = gid
                driver = self.driver
                driver.set_page_load_timeout(self.wait)
                self.dwait(self.wait)
                id = random.randint(1, 1000000)
                post_text = f"#1 {str(id)}"

                try:
                    test_start_time = datetime.datetime.now()
                    Vk.vk_login(self, self.wait)
                    self.supress_wait_8_sec(driver.get(f"https://vk.com/club{gid}"))
                    self.find("//div[@id='post_field']").clear()
                    sleep(1)
                    self.find("//div[@id='post_field']").send_keys(post_text)
                    sleep(1)
                    self.if_click("//button[@id='send_post']", "ok отправка поста на стену", "fail отправка поста на стену")
                    sleep(10)
                    Vk.check_delivery(self, msg=id, gid=gid, t_check=self.t_check)


                except Exception as e:
                    self.pars_err(f"fail ошибка выполнения скрипта, {e}")

                try:
                    self.inter_result['comment'] += f"\nОписание________ gid {gid}, скрипт делает пост на стене от лица сообщества в сообществе " \
                                                f"{gid} и проверяет приход сообщения в диалоге, максимальное ожидание {self.t_check}"
                except Exception as e:
                    self.pars_err(f"fail ошибка добавления описания теста в словарь, {e}")

                self.test_ending()

                if self.inter_result['result'] == 0:
                    return "ok"
                else:
                    return f'fail, {self.inter_result["error"]}'

if __name__ == '__main__':
    for i in range(1):

        print(f"gid {gid}, started at ", time.strftime('%H:%M:%S').replace("'", ""))
        try:
            test_obj = Hashtag().test()
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")


