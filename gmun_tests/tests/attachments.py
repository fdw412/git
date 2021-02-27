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


gid = 190158182
uid=585675
topic_id = 632050
token = token_ms_chain_2020_gid_191083897

no_driver = False
silent = False
attachment="photo585675_456239591 video-161493867_456239018 audio_playlist-2266_85402640 audio-161493867_456239017 wall-161493867_1 market-161493867_1487283 doc-161493867_466345806"


class Attachments(GmunTest):
    def __init__(self):
        self.name = 'Attachments'
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

                Vk.vk_login(self, self.wait)
                id = random.randint(1, 1000000)
                message = f"0 attachments test, message {id}"
                driver.set_page_load_timeout(self.wait)
                driver.implicitly_wait(self.wait)

                driver.get(f"https://vk.com/app5728966_-{gid}")
                Vk.get_frame(self)
                sleep(1)
                self.find(".//a[text()='Создание рассылки']").click()
                sleep(1)
                self.find(".//div[contains(text(), 'Выберите тему')]").click()
                sleep(1)
                self.find(".//div[contains(text(), '1')]").click()
                sleep(1)
                self.find(".//textarea[contains(@class, 'sc-')]").clear()
                sleep(1)
                self.find(".//textarea[contains(@class, 'sc-')]").send_keys(message)
                sleep(1)
                self.find(
                    ".//span[text()='Список ссылок на VK материалы']/parent::button[1]").click()
                sleep(1)
                self.find(".//textarea[@id='.attachments']").clear()
                sleep(1)
                self.find(".//textarea[@id='.attachments']").send_keys(attachment)
                sleep(1)
                self.find(".//button[contains(text(), 'Запустить рассылку')]").click()

                try:
                    if self.inter_result["result"] != 1:
                        with suppress(Exception):
                            self.driver.get(f"https://vk.com/im?sel=-{gid}")
                        sleep(1)
                    datetime1 = datetime.datetime.now()
                    for i in range(round(self.t_check/10)+3):
                        self.driver.refresh()

                        self.dwait(1)
                        with suppress(Exception):
                            self.find(".// *[contains(text(), 'Перейти в конец истории')]").click()
                        sleep(1)
                        self.dwait(2)
                        temp = str()


                        delta = abs(round((datetime1 - datetime.datetime.now()).total_seconds()))

                        if self.ifis_no_exception(f".//div[contains(text(), '{id}')]") == True:
                            temp = temp + 'сообщение пришло, '
                        else:
                            temp = temp + f"fail сообщение не найдено в диалоге, ожидание {delta} сек., "

                        if self.ifis_no_exception(f".//div[contains(text(), '{id}')]/div/div/a[contains(@aria-label, 'фотография')]") == True:
                            temp = temp + 'фото пришло, '
                        else:
                            temp = temp + f"fail фото не найдено, ожидание {delta} сек. "

                        if self.ifis_no_exception(f".//div[contains(text(), '{id}')]/div/div/a[contains(@href, 'video-161493867_456239018')]") == True:
                            temp = temp + 'видео пришло, '
                        else:
                            temp = temp + f"fail видео не найдено, ожидание {delta} сек. "

                        if self.ifis_no_exception(f".//div[contains(text(), '{id}')]/div/div[contains(@class, 'im_msg_media im_msg_media_audio_playlist')]/div[contains(@class, '2266_85402640')]") == True:
                            temp = temp + 'плейлист пришел, '
                        else:
                            temp = temp + f"fail плейлист не пришел, ожидание {delta} сек., "

                        if self.ifis_no_exception(f".//div[contains(text(), '{id}')]/div/div/div[contains(@data-audio, 'Outfit')]") == True:
                            temp = temp + 'аудио пришло, '
                        else:
                            temp = temp + f"fail аудио не найдено, ожидание {delta} сек. "

                        if self.ifis_no_exception(f".//div[contains(text(), '{id}')]/div/div[contains(@class, 'im_msg_media im_msg_media_wall')]/div[contains(@id, 'post-161493867_1')]") == True:
                            temp = temp + 'пост на стене пришел, '
                        else:
                            temp = temp + f"fail пост на стене не пришел, ожидание {delta} сек. "

                        if self.ifis_no_exception(f".//div[contains(text(), '{id}')]/div/div[contains(@class, 'im_msg_media im_msg_media_market')]") == True:
                            temp = temp + 'товар пришел, '
                        else:
                            temp = temp + f"fail товар не пришел, ожидание {delta} сек. "

                        if self.ifis_no_exception(f'.//div[contains(text(), "{id}")]/div/div[contains(@class, "media_doc")]') == True:
                            temp = temp + 'документ пришел, '
                        else:
                            temp = temp + f"fail документ не пришел, ожидание {delta} сек. "

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
                    self.pars_err(f"fail ошибка при проверке сообщений в диалоге, {e}")



            except Exception as e:
                self.pars_err(f"fail ошибка выполнения скрипта, {e}")

            try:
                self.inter_result['comment'] += f"\nОписание________ gid {gid}, скрипт отправляет сообщение через фронт с вложениями, " \
                                                f"и ждет их появление в диалоге, максимальное ожидание {self.t_check}"
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
            test_obj = Attachments().test()
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")


