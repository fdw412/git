# -*- coding: utf-8 -*-
import datetime, time, re
from gmun_tests import GmunTest
from gmun_tests.utils.mattermost import Mattermost, channel_test_fails, channel_town_square, channel_no_alert
from time import sleep
from contextlib import suppress
import random

silent = False


class Sender_Statuses(GmunTest):
    def __init__(self):
        self.name = 'Sender_Statuses'
        self.mattermost = Mattermost()
        GmunTest.__init__(self, name=self.name, no_driver=False)
        self.silent = silent or True
        self.wait = 60

    def login(self):
        for i in range(1, 3):
            try:
                self.driver.get(f"https://sender.antipsy.ru/admin/")
                if self.ifis_no_exception("//label[@for='id_username']", wait=3):
                    self.driver.find_element_by_xpath("//*[@name='username']").send_keys("admin")
                    self.driver.find_element_by_xpath("//*[@name='password']").send_keys("VORONAbrosay2223322")
                    self.driver.find_element_by_xpath("//*[@type='submit']").click()
                    break
                elif self.ifis_no_exception("//h1[contains(text(), 'Site administration')]", wait=3):
                    break
            except Exception as e:
                print(e)


    def get_params(self, dict):
        self.delta_hours_created = self.get_delta(dict['Created']) or None
        self.delta_hours_updated = self.get_delta(dict['Updated']) or None
        self.delta_hours_started = self.get_delta(dict['Started']) or None
        self.delta_hours_finished = self.get_delta(dict['Finished']) or None
        self.created = dict['Created'] or None
        self.updated = dict['Updated'] or None
        self.started = dict['Started'] or None
        self.finished = dict['Finished'] or None
        self.status = dict['Status'] or None
        try:
            self.attempts = int(dict['Attempts']) or None
        except Exception:
            self.attempts = None

        try:
            self.expected = int(dict['Expected']) or None
        except Exception:
            self.expected = None

        try:
            self.mid = int(dict['Mid']) or None
        except Exception:
            self.mid = None

        try:
            self.gid = int(dict['Gid']) or None
        except Exception:
            self.gid = None

        try:
            self.delivered = int(dict['Delivered']) or None
        except Exception:
            self.delivered = None

        # print(f"gid {self.gid}, expected {self.expected}, mid {self.mid}, "
        #       f"delta_created {self.delta_hours_created}, "
        #       f"delta_updated {self.delta_hours_updated}, "
        #       f"delta_started {self.delta_hours_started}, "
        #       f"delta_finished {self.delta_hours_finished},\n "
        #       f"created = {self.created}, "
        #       f"updated = {self.updated}, "
        #       f"started = {self.started}, \n"
        #       f"finished = {self.finished}, "
        #       f"attempts = {self.attempts}, "
        #       f"expected {self.expected}, "
        #       f"delivered {self.delivered}")

    def get_delta(self, string):

        temp = re.search("^(.){3}. \d{1,2}", string)
        if temp and len(string) > 10:
            Day = int(str(temp.group(0)[-3:]).replace(" ", "").replace(".", "").replace(",", ""))
        else:
            Day = None

        temp = re.search("\d{1,2}:", string)
        if temp and len(string) > 10:
            Hour = str(temp.group(0)[:2]).replace(":", "").replace(".", "").replace(",", "")
            if str(temp).find("p.m."):
                daypart = "PM"
            elif str(temp).find("a.m."):
                daypart = "AM"
        else:
            Hour = None
            daypart = None

        if Hour and daypart:
            Hour = Hour+daypart
            Hour = int(datetime.datetime.strptime(Hour, '%I%p').strftime("%H"))

        temp = re.search("\d{4}", string)
        if temp and len(string) > 10:
            Year = int(temp.group(0))
        else:
            Year = None

        if Year and Day and Hour:
            item_time = datetime.datetime.now().replace(year=Year, day=Day, hour=Hour)
            now = datetime.datetime.now()
            delta_hours = round((now - item_time).total_seconds() / 3600)
        else:
            delta_hours = None

        return delta_hours

    def fill_list(self, url, count):
        list = []
        if not self.ifis_no_exception("//p[contains(text(), '0 mailings')]", wait=1):
            for i in range(1, count):
                path = f'//table[@id="result_list"]/tbody/tr[contains(@class, "row")][{i}]'
                if self.ifis_no_exception(path, wait=0):
                    dict = {}
                    dict['Mid'] = self.find(f'{path}/th[@class="field-id"]/a', wait=0).get_attribute(
                        "text") or None
                    dict['Created'] = self.find(f'{path}/td[@class="field-created_at nowrap"]',
                                                wait=0).get_attribute("innerHTML") or None
                    dict['Updated'] = self.find(f'{path}/td[@class="field-updated_at nowrap"]', wait=0).get_attribute(
                        "innerHTML") or None
                    dict['Started'] = self.find(f'{path}/td[@class="field-started_at nowrap"]', wait=0).get_attribute(
                        "innerHTML") or None
                    dict['Finished'] = self.find(f'{path}/td[@class="field-finished_at nowrap"]', wait=0).get_attribute(
                        "innerHTML") or None
                    dict['Status'] = self.find(f'{path}/td[@class="field-get_status"]/a', wait=0).get_attribute(
                        "text") or None
                    dict['Attempts'] = self.find(f'{path}/td[@class="field-get_workers_attempted"]',
                                                 wait=0).get_attribute("innerHTML") or None
                    dict['Gid'] = self.find(f'{path}/td[@class="field-gid"]', wait=0).get_attribute("innerHTML") or None
                    dict['Expected'] = self.find(f'{path}/td[@class="field-get_expected_msg_count"]',
                                                 wait=0).get_attribute("innerHTML") or None
                    dict['Delivered'] = self.find(f'{path}/td[@class="field-get_delivered_msg_count"]',
                                                  wait=0).get_attribute("innerHTML") or None
                    list.append(dict)
                else:
                    break
        return list

    def check_in_progress(self, gid):
        url = f"https://sender.antipsy.ru/admin/mailings/mailing/?status__exact=in+progress&created_at__gt={self.date}&source__source_id=2&gid={gid}"
        self.driver.get(url)
        return not self.ifis_no_exception("//p[contains(text(), '0 mailings')]", wait=1)

    def test(self, paused=False):
        print(f'Sender_statuses 1')
        driver = self.driver
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(self.wait)
        text = ""
        print(f'Sender_statuses 2')

        try:
            self.date = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
            test_start_time = datetime.datetime.now()
            self.login()
            print(f'Sender_statuses 3')


            ##################################################### проверка в статусе new
            url = f"https://sender.antipsy.ru/admin/mailings/mailing/?status__exact=new&created_at__gt={self.date}&source__source_id=2&o=12"
            driver.get(url)
            list = self.fill_list(url, count=5)
            temp = ""
            for dict in list:
                self.get_params(dict)
                if self.delta_hours_created and self.attempts and self.expected and self.mid and self.gid:
                    if self.delta_hours_created > 8:
                        if self.check_in_progress(gid=self.gid) != True:
                            temp+=f'рассылка на {self.expected} получателей находится статусе **new** более {self.delta_hours_created} часов, ' \
                                  f'mid {self.mid}, gid {self.gid}, created {self.created}, started {self.started}, attemts {self.attempts}\n ' \
                                  f'другие рассылки данных сообществ в статусе in progress не найдены\n'
            if len(temp) >1:
                text = text + temp + "весь список рассылок в статусе **new** https://sender.antipsy.ru/admin/mailings/mailing/?status__exact=new\n\n"


            ####################################### проверка в in progress

            url = f"https://sender.antipsy.ru/admin/mailings/mailing/?status__exact=in+progress&created_at__gt={self.date}&source__source_id=2&o=14"
            driver.get(url)
            list = self.fill_list(url, count=5)
            temp = ""
            for dict in list:
                self.get_params(dict)
                if self.delta_hours_started and self.attempts and self.expected and self.mid and self.gid:
                    if self.delta_hours_started > 8 and self.expected < 500000:
                            temp+=f'рассылка на {self.expected} получателей находится статусе **in progress** более {self.delta_hours_created} часов\n' \
                                  f'mid {self.mid}, gid {self.gid}, created {self.created}, started {self.started}, attemts {self.attempts}\n'

            if len(temp) >1:
                text = text + temp + f'посмотреть все рассылки в статусе **in proigress** https://sender.antipsy.ru/admin/mailings/mailing/?source__source_id=2&status__exact=in+progress\n\n'



            if len(text) >1:
                msg = "**#Sender_statuses**\n" + text
                self.last_call_get()
                self.time_delta_minutes_count()
                temp = self.time_delta_minutes
                if self.time_delta_minutes > 60*24:
                    msg = text
                    self.mattermost.create_post(channel_town_square, msg)
                    self.last_call_set()

            else:
                msg = "ok **#Sender_statuses**"
                self.mattermost.create_post(channel_no_alert, msg)

            print(msg)
            print(f'Sender_statuses 4')

        except Exception as e:
            print("Sender_statuses\n" + e)

        with suppress(Exception):
            self.driver.quit()


from celery import Celery
from gmun_tests.settings.celery import CELERY_BROKER_URL
app = Celery('gmun_tests', broker=CELERY_BROKER_URL)
from celery.exceptions import SoftTimeLimitExceeded
from gmun_tests.utils.mattermost import Mattermost



@app.task(soft_time_limit=1700, time_limit=1800, name='sender_statuses')
def sender_statuses():
    try:
        Sender_Statuses().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"sender_statuses, {e}")

with suppress(Exception):
    app.control.purge()

app.conf.beat_schedule = {
'sender_statuses': {'task': 'sender_statuses','schedule': 8*3600, 'options': {'queue': 'sender_statuses'}}
}




if __name__ == '__main__':
        print("started at ", time.strftime('%H:%M:%S').replace("'", ""))
        try:
            test_obj = Sender_Statuses().test()
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")


