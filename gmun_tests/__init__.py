import os
import time
import urllib3
import redis
import json
import random
import requests
import datetime
from time import sleep
from gmun_tests.settings import logger, app_id_prod
from selenium.webdriver.common.keys import Keys
from gmun_tests.debug_info import timedelta_sms_value
from contextlib import suppress

from gmun_tests.settings.selenium import config_profile, CHROMEDRIVER_PATH

from selenium.common.exceptions import NoSuchElementException

from gmun_tests.settings import (
    SCREENSHOT_PATH,
    SCREENSHOT_TIME_FORMAT,
    DEFAULT_RUN_SERIES_COUNT,
    DEFAULT_FAIL_LIMIT_COUNT,
    GMUN_IFRAME,
    GMUN_IFRAME_DEV
)

from selenium import webdriver
from gmun_tests.settings.celery import (
    REDIS_HOST, REDIS_PORT, REDIS_DB_NUMBER, REDIS_PASSWORD,
)

from contextlib import suppress


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



class GmunTest:
    def __init__(self, no_driver=False, name='GmunTestTemplate'):
        self.dev = False
        self.no_driver = no_driver
        self.no_sms  = False
        self.name = name
        self.last_call = f'\"{int(time.time())}\"'
        self.last_call_main = f'\"{int(time.time())}\"'
        self.driver_options = config_profile(self.name)
        self.random_id = f'{random.randint(1, 1000000)}'
        self.max_retry_count = 3
        self.sms_notify_time_repeat = 30 * 60  # in seconds
        self.redis = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB_NUMBER,
            password=REDIS_PASSWORD,
        )
        self.last_call_name = f"{self.name}_last_call"
        self.alert = False
        self.inter_result = {}
        self.redis_results_chain = []
        self.inter_result['results_line'] = []
        self.inter_result['results_line_datetime'] = []
        self.inter_result['result'] = 0
        self.inter_result['error'] = ""
        self.inter_result['screen_paths'] = []
        self.inter_result['comment'] = ""

        self.silent = False
        self.timedelta_sms_value = timedelta_sms_value
        if self.no_driver != True:
            self.init_webdriver()

        self.time_delta_minutes = 999999
        self.time_delta_last_call_main_minutes = 999999
        self.app_id = app_id_prod


        self.channel_alerts = 'kcm8c64scb8djp6rd6wfmyspnh'  # Tests with alerts
        self.channel_fails = 'r1y5g4jnqbrdipiyc4aypg16cc'  # test fails
        self.channel_town_square = 'k4u43q3jrfrh8citcjsnc1ebqw'  # town square
        self.channel_no_alerts = 'fkipqeakxjnm7b9jb1o7p7t4we'  # Tests with no alerts

    def init_webdriver(self):
        self.driver = webdriver.Chrome(
            CHROMEDRIVER_PATH, chrome_options=self.driver_options)
        sleep(1)
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(180)
        self.driver.set_script_timeout(600)
        self.driver.desired_capabilities.update({'pageLoadStrategy': 'none'})
        clear = datetime.datetime.now().strftime("%d-%H")
        if clear == '01-03':
            with suppress(Exception):
                self.driver.get('chrome://settings/clearBrowserData')
                self.driver.find_element_by_xpath('//settings-ui').send_keys(Keys.ENTER)

    def test(self, *args, **kwargs):
        pass

    def addcom(self, arg):
        self.inter_result['comment'] = str(self.inter_result['comment'] + f"{arg}, ").replace(", ,", "")

    def adderr(self, arg):
        self.inter_result['error'] += f"\n**ERROR____________** {arg}\n".replace(", ,","")

    def addscr(self):
        if self.no_driver != True:
            driver = self.driver
            screenshot = f"{SCREENSHOT_PATH}\\{datetime.datetime.now().strftime(SCREENSHOT_TIME_FORMAT)}.png"
            driver.save_screenshot(screenshot)
            self.inter_result['screen_paths'].append(screenshot)

    def pars_err(self, add, noscreen=False):
            str(add).replace("\n,","\n")
            self.inter_result['result'] = 1
            self.adderr(add)
            # self.addcom(add)
            if not noscreen:
                self.addscr()

    def run(self, *args, **kwargs):
        self.test(*args, **kwargs)
        if self.no_driver != True:
            self.driver.quit()

    def set_result(self):
        result = f'{self.inter_result["result"]}:{int(time.time())}'
        try:
            self.inter_result['comment'] = str(self.inter_result['comment']).replace("\n,", "").replace("\n, ", "")
            self.inter_result['error'] = str(self.inter_result['error']).replace("\n,", "").replace("\n, ", "")

            self.redis_results_chain = json.loads(self.redis.get(self.name) or '[]') or []
            if len(self.redis_results_chain) >= self.run_series_count:
                self.redis_results_chain = self.redis_results_chain[:self.run_series_count]
            self.redis_results_chain.insert(0, result)
            self.redis.set(self.name, json.dumps(self.redis_results_chain))

            for i in self.redis_results_chain:
                self.inter_result['results_line'].append(int(str(i)[0]))
                if int(str(i)[0]) == 0:
                    a = " ок"
                else:
                    a = " fail"
                self.inter_result['results_line_datetime'].append(
                    f"{datetime.datetime.fromtimestamp(int(i[2:])).strftime('%H:%M')}{a}")

            self.inter_result['results_line_datetime'] = \
                "_" + str(self.inter_result['results_line_datetime'])\
                    .replace("'","").replace("[","").replace("]","") + "_"

        except Exception as e:
            message = f"Script Error, метод set_result, тест {self.name}." \
                      f"это сообщение значит, что скрипт не достучался к Redis " \
                      f"и в случае реальных фейлов может не отправить " \
                      f"смс и сообщение в общий чат\n{e}"
            if self.silent == True:
                print(message)
            else:
                channel_id = 'k4u43q3jrfrh8citcjsnc1ebqw' # town square
                self.mattermost.create_post(channel_id, message)

    # last_call_mian это когда по любому тесту был алерт, а last_call когда по кокнкретному тесту был алерт
    def last_call_set(self):
        try:
            self.redis.set(self.last_call_name, json.dumps(str(int(time.time()))))
            self.redis.set('last_call_main', json.dumps(str(int(time.time()))))
        except Exception as e:
            message = f"error last_call_set, тест {self.name}\n{e}"
            if self.silent == True:
                print(message)
            else:
                pass

    def last_call_main_set(self):
        try:
            self.redis.set('last_call_main', json.dumps(str(int(time.time()))))
        except Exception as e:
            message = f"error last_call_main_set, тест {self.name}\n{e}"
            if self.silent == True:
                print(message)
            else:
                pass

    def last_call_get(self):
        str(time.time())
        try:
            self.last_call = self.redis.get(self.last_call_name)
            self.last_call_main = self.redis.get('last_call_main')

            if self.last_call == None:
                self.last_call = str(int(time.time()))
                self.last_call_set()
            else:
                self.last_call = self.last_call.decode()

            if self.last_call_main == None:
                self.last_call_main = str(int(time.time()))
                self.last_call_main_set()
            else:
                self.last_call_main = self.last_call_main.decode()

        except Exception as e:
            message = f"error last_call_get, тест {self.name}\n{e}"
            if self.silent == True:
                print(message)
            else:
                pass

    def count_alert(self):
        results_line = self.inter_result['results_line']
        if results_line[:self.fail_limit_count].count(1) == self.fail_limit_count and results_line[self.fail_limit_count:].count(1) == 0:
            self.alert = True
        else:
            self.alert = False

    def get_result(self, pos=None):
        try:
            self.redis_results_chain = json.loads(self.redis.get(self.name))
            pos = pos and isinstance(pos, int) and pos < len(self.redis_results_chain) or -1
            return self.redis_results_chain[pos]
        except Exception as e:
            message = f"Script Error, метод get_result, тест {self.name}, " \
                      f"это сообщение значит, что скрипт не достучался к Redis " \
                      f"и в случае реальных фейлов может не отправить " \
                      f"смс и сообщение в общий чат, \n{e}"
            if self.silent == True:
                print(message)
            else:
                channel_id = 'k4u43q3jrfrh8citcjsnc1ebqw' # town square
                self.mattermost.create_post(channel_id, message)


    def send_sms(self, text, name=None):
        try:
            print("---SMS---ОТПРАВКА---SMS---")
            token = "EFA37D94-F152-3965-C80C-76DCF44352EC"
            contacts={'ss8545':79522186234, 'alexandr':79319886866}
            # 'sergey': 79117183625,
            for i in contacts:
                url = f"https://sms.ru/sms/send?api_id={token}&to={contacts[i]}&msg={text}"
                r = requests.post(url, timeout=30, verify=False)
                print(i, r.text)
                time.sleep(1)

            self.last_call_main_set()
            self.last_call_set()


        except Exception as  e:
                print("отправка sms", e)

    def ifis_no_exception(self, xpath, wait = 0.5):
        self.dwait(wait)
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException as e:
            self.driver.implicitly_wait(self.wait)
            return False
        self.driver.implicitly_wait(self.wait)
        return True

    def find(self, xpath, wait = -1):
        if wait >= 0:
            self.driver.implicitly_wait(wait)
        else:
            sleep(1)
        try:
            el = self.driver.find_element_by_xpath(xpath)
            self.driver.implicitly_wait(self.wait)
            return el
        except Exception as e:
            self.driver.implicitly_wait(self.wait)
            raise

    def dwait(self, sec=7):
        self.driver.implicitly_wait(sec)

    def supress_wait_8_sec(self, func):
        self.dwait(8)
        try:
            func
            self.dwait(self.wait)

        except Exception as e:
            self.adderr(e)
            self.addcom(e)
            self.addscr()
            self.dwait(self.wait)

    def if_click(self, xpath, text_ok="", text_fail="", wait=False):
        if wait:
            self.dwait(wait)
        for i in range(2):
            sleep(1)
            try:
                self.driver.find_element_by_xpath(xpath).click()
                self.addcom(text_ok)
                break
            except Exception:
                if i == 1:
                    self.addcom(text_fail)
                    self.adderr(text_fail)
                    raise
                else:
                    pass

        self.dwait(self.wait)


    def if_only_one_screen(self):
        with suppress(Exception):
            if len(self.inter_result['screen_paths']) == 1:
                if os.path.exists(f"{SCREENSHOT_PATH}\\___none.png") == True:
                    self.inter_result['screen_paths'].append(f"{SCREENSHOT_PATH}\\___none.png")

    def send_regular_mattermost_alerts(self):
        try:
            if self.no_sms:
                channel_id = self.channel_no_alerts
            else:
                channel_id = self.channel_alerts

            if self.inter_result['result'] ==0:
                message = f"**ok** #{self.name},  {self.inter_result['results_line_datetime']}"
                self.mattermost.create_post(channel_id, message)

            else:
                message = f"**fail** #{self.name}\n{self.inter_result['error']}\n{self.inter_result['results_line_datetime']}\n{self.inter_result['comment']}"
                self.mattermost.create_post(channel_id, message, self.inter_result['screen_paths'])
                self.mattermost.create_post(self.channel_fails, message, self.inter_result['screen_paths']) # test fails

        except Exception as e:
            print("ошибка при отправке в mattermost", e)

    def time_delta_minutes_count(self):
        now = datetime.datetime.now()

        last_call = datetime.datetime.fromtimestamp(int(str(self.last_call).replace("\"", "")))
        self.time_delta_minutes = round(abs((now - last_call).total_seconds() / 60))

        last_call_main = datetime.datetime.fromtimestamp(int(str(self.last_call_main).replace("\"", "")))
        self.time_delta_last_call_main_minutes = round(abs((now - last_call_main).total_seconds() / 60))

    def send_alarm_alerts(self):
        try:

            sms = f"{self.name}+failed+{self.fail_limit_count}+times+in+a+row"
            msg = f"@channel\n#{self.name} failed {self.fail_limit_count} times in a row \n{self.inter_result['error']}" \
                  f"\n{self.inter_result['comment']}\n{self.inter_result['results_line_datetime']}"

            if self.alert:
                if not self.silent:
                    # town square
                    channel_id = self.channel_town_square
                else:
                    print("___case to send alarm alerts but silent is true___")
                    # test fails
                    channel_id = self.channel_fails

                self.mattermost.create_post(channel_id, msg, self.inter_result['screen_paths'])

                if self.time_delta_last_call_main_minutes > self.timedelta_sms_value:
                    if not self.no_sms:
                        if not self.silent:
                            self.send_sms(text=sms)

        except Exception as e:
            print("ошибка при отправке в town square и sms", e)

    def send_delayed_alerts(self):
            try:
                percent_limit = 70
                delay_minutes = 180
                results_line = self.inter_result['results_line']
                if results_line.count(1)/self.run_series_count  >= percent_limit/100 and self.time_delta_minutes > delay_minutes:
                    send_msg=True
                else:
                    send_msg=False

                msg = f"@channel\n Повторные уведомления, #{self.name} удельное кол-во фейлов {percent_limit}%" \
                      f"\n{self.inter_result['error']}\n{self.inter_result['results_line_datetime']}\n\n{self.inter_result['comment']}"
                if send_msg  == True:

                    if self.silent == False:
                        # town square
                        channel_id = self.channel_town_square
                    else:
                        # test fails
                        channel_id = self.channel_fails

                    self.mattermost.create_post(channel_id, msg, self.inter_result['screen_paths'])
                    self.last_call_set()

            except Exception as e:
                print(e)

            # отправка смс
            try:
                percent_limit = 70
                delay_minutes = 480
                results_line = self.inter_result['results_line']
                if results_line.count(1)/self.run_series_count  >= percent_limit/100 and self.time_delta_last_call_main_minutes > delay_minutes:
                    send_msg=True
                else:
                    send_msg=False

                sms = f"{self.name}+fails+more+{percent_limit}+percents,+message+repeats+every+{delay_minutes} min"
                if send_msg:
                    if not self.no_sms:
                        if not self.silent:
                            self.send_sms(text=sms)

            except Exception as e:
                print(e)

    def test_ending(self):

        if not self.dev:
            try:
                self.last_call_get()
            except Exception as e:
                print(e)

            with suppress(Exception):
                if not self.no_driver:
                    self.driver.quit()

            self.if_only_one_screen()

            try:
                self.set_result()
            except Exception as e:
                self.pars_err(f"ошибка set_result, {e}")

            try:
                self.count_alert()
            except Exception as e:
                print(f"ошибка count_alert, {e}")

            try:
                self.time_delta_minutes_count()
            except Exception as e:
                self.pars_err(f"ошибка time_delta_minutes_count, {e}")

            try:
                self.send_regular_mattermost_alerts()
            except Exception as e:
                print(f"ошибка send_regular_mattermost_alerts, {e}")

            try:
                self.send_alarm_alerts()
            except Exception as e:
                print(f"ошибка send_alarm_alerts, {e}")

            try:
                self.send_delayed_alerts()
            except Exception as e:
                print(f"ошибка send_delayed_alerts, {e}")

        if not self.dev:
            print(self.name, " result: ", self.inter_result["result"], f" {self.inter_result['results_line_datetime']}")
        else:
            print(self.name, " result: ", self.inter_result["result"])

        if self.inter_result["error"]:
            print("ERROR ", self.inter_result["error"])
        print("comment ", self.inter_result["comment"])
        print("finished at ", time.strftime('%H:%M:%S').replace("'", ""))
        print()


    def pause(self):
        if self.inter_result['result'] == 0:
            sleep(self.t_check+30)

