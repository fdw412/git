from selenium.common.exceptions import NoSuchElementException
import requests, time, json, random
from time import sleep
from contextlib import suppress
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from gmun_tests.settings import SCREENSHOT_PATH, SCREENSHOT_TIME_FORMAT, vk_user_login, vk_user_password, app_id_prod, user_id, GMUN_IFRAME_DEV, GMUN_IFRAME
from gmun_tests import GmunTest
import datetime
requests.packages.urllib3.disable_warnings()

class Vk(GmunTest):
    def __init__(self):
        GmunTest.__init__(self)
        self.driver

    def vk_login(self, wait, user = vk_user_login, password = vk_user_password):

        sleep(1)
        for i in range(0,2):
            try:
                self.supress_wait_8_sec(self.driver.get(f"https://vk.com"))
                sleep(1)

                xpath = ".//*[contains(@class, 'cookies_policy_close')]"
                if self.ifis_no_exception(xpath):
                    with suppress(Exception):
                        self.driver.find_element_by_xpath(xpath).click()
                    sleep(1)
                    self.driver.refresh()
                    sleep(1)

                xpath = ".//*[contains(@class, 'OldBrowser__close')]"
                if self.ifis_no_exception(xpath):
                    with suppress(Exception):
                        self.driver.find_element_by_xpath(xpath).click()
                    sleep(1)
                    self.driver.refresh()
                    sleep(1)


                if self.ifis_no_exception(".//*[contains(text(), 'Подумайте о безопасности')]"):
                    with suppress(Exception):
                        self.driver.find_element_by_xpath(".//*[contains(text(), 'Подтвердить')]").click()
                    sleep(1)
                    self.driver.refresh()
                    sleep(1)

                if self.ifis_no_exception(".//span[contains(text(), 'Моя страница')]"):
                    self.addcom("vk login ok")
                    break
                else:
                    if self.ifis_no_exception(".//button[@id='index_login_button']") == True:
                        self.find(".//input[@id='index_email']").send_keys(user)
                        self.find(".//input[@id='index_pass']").send_keys(password)
                        self.find(".//button[@id='index_login_button']").click()
                        sleep(2)
                        self.driver.refresh()
                        break
                    else:
                        if i == 1:
                            self.pars_err("vk login fail не удалось найти кнопку входа во время загрузки vk.com")



            except Exception as e:
                self.pars_err(f"vk login fail, {str(e)}", noscreen=True)
                raise

        self.dwait(wait)
        return self.inter_result

    def msg_deny(self, gid):
        if not self.dev:
            urlpart = 'mp.gmun.pro'
        else:
            urlpart = 'vkmul.dev.antipsy.ru'
        url = f"https://{urlpart}/api/callback/vk/response/4b9b03a06fd74357b7361a929f0ae708/"

        if self.inter_result['result'] !=1:

            payload = "{\"type\":\"message_deny\",\"object\":{\"user_id\":%s},\"group_id\":%s}" %(user_id, gid)
            headers = {'content-type': "application/json"}
            try:
                r = requests.post(url, headers=headers, data=payload, verify=False)
                r2 = r.status_code
                if r2 == 200:
                    self.addcom('ok запрос на отписку от всех тем к mp.gmun.pro принят')
                else:
                    self.pars_err(f'fail запрос на отписку от всех тем к mp.gmun.pro, {r2}', noscreen=True)

            except Exception as e:
                self.pars_err(f"fail запрос на отписку от всех тем к mp.gmun.pro, Exception {str(e)}", noscreen=True)
                raise

    # через gmun api не работает пока
    # def unsubscribe(self, gid, uid, topic_id, token):
    #     if self.inter_result['result'] !=1:
    #         url = f"https://api.gmun.pro/api/1/subscription/UnSubscribe?group_id={gid}&user_id={uid}&topic_id={topic_id}&access_token={token}"
    #         try:
    #             r = requests.get(url, verify=False).text
    #             if r.find("task successfully received") != -1:
    #                 self.addcom(f'ok запрос на отписку от темы {topic_id} через gmun api принят успешно')
    #             else:
    #                 self.pars_err(f'fail \nresponse.text:{r}', noscreen=True)
    #
    #         except Exception as e:
    #             self.pars_err(f"fail запрос на отписку от темы через gmun api, Exception {str(e)}", noscreen=True)
    #             raise

    def unsubscribe(self, gid, uid, topic_id, token=None):
        if self.inter_result['result'] !=1:
            if not self.dev:
                urlpart = "interlayer-subscription.antipsy.ru"
                authkey = "226c594ef87cfd12971ac9afdab41b49"
            else:
                urlpart = "interlayer-subscription.dev.antipsy.ru"
                authkey = "226c594ef87cfd12971ac9afdab41b49"

            url = f"https://{urlpart}/unsubscribe/"
            json = {"group_id": gid, "user_id": uid, "theme_id":topic_id, "auth_key": authkey}
            headers = {'content-type': "application/json"}

            try:
                r = requests.post(url, verify=False, headers = headers, json = json).json()
                if str(r).find("далено") != -1:
                    self.addcom(f'ok запрос на отписку от темы {topic_id} через interlayer принят успешно')
                else:
                    self.pars_err(f'fail запрос на отписку от темы {topic_id} через interlayer\nresponse.text:{r}', noscreen=True)

            except Exception as e:
                self.pars_err(f"fail запрос на отписку от темы через interlayer, Exception {str(e)}", noscreen=True)

    def check_subscription_subsman(self, gid, uid, topic_id):
        if self.inter_result["result"] != 1:
            try:
                t1 = datetime.datetime.now()
                devider = 12
                for i in range(devider):
                    url = f"https://subscription-manager.antipsy.ru/groups/{gid}/topics/{topic_id}/subscriptions/"
                    headers = {
                        'Authorization': 'Token 8af0e450435eba53a9357f999b0e39a47a0d9987'
                    }
                    r = requests.request("GET", url, headers=headers)
                    a = r.status_code
                    b = str(r.content).strip('b\'[]')
                    if a == 200 and b.find(f"{uid}") != -1:
                        self.addcom(f"ok проверка подписки на тему {topic_id} запросом к subsman, ")
                        return True
                    else:
                        if i == (devider-1):
                            self.pars_err(
                                f"fail проверка подписки на тему {topic_id} "
                                f"ожидание {round((datetime.datetime.now() - t1).total_seconds())} сек.")
                            return False
                    sleep(5)


            except Exception as e:
                self.pars_err(f"fail проверка подписки на тему, {e}", noscreen=True)

    def check_unsubscription_subsman(self, gid, uid, topic_id, fast=False):
        if self.inter_result["result"] != 1:
            try:
                t1 = datetime.datetime.now()
                if fast == True:
                    devider = 1
                else:
                    devider = 12

                for i in range(devider):
                    url = f"https://subscription-manager.antipsy.ru/groups/{gid}/topics/{topic_id}/subscriptions/"
                    headers = {
                        'Authorization': 'Token 8af0e450435eba53a9357f999b0e39a47a0d9987'
                    }
                    r = requests.request("GET", url, headers=headers)
                    a = r.status_code
                    b = str(r.content).strip('b\'[]')
                    if a == 200 and b.find(f"{uid}") == -1:
                        self.addcom("ok проверка отписки от темы")
                        return True
                    else:
                        if i == (devider-1):
                            if fast != True:
                                self.pars_err(
                                    f"fail проверка отписки от темы {topic_id} запросом к subsman, "
                                    f"ожидание {round((datetime.datetime.now() - t1).total_seconds())} сек.", noscreen=True)
                            return False
                    sleep(5)


            except Exception as e:
                self.pars_err(f"fail проверка отписки от темы, {e}", noscreen=True)


    def check_subscription(self, gid, uid, topic_id):
        if self.inter_result["result"] != 1:
            try:
                t1 = datetime.datetime.now()
                devider = 24
                if not self.dev:
                    urlpart = 'gmun.pro'
                else:
                    urlpart = 'gmun-php.dev.antipsy.ru'

                url = f"https://{urlpart}/api/callback/vk/groups/get-users-by-topic-id?access_token=fGftE=lTXF]DeSnX5ztDm&gid={gid}&topic_id[]={topic_id}"

                for i in range(devider):


                    r = requests.request("GET", url)
                    a = r.status_code
                    b = str(r.content).strip('b\'[]')
                    if a == 200 and b.find(f"{uid}") != -1:
                        self.addcom(f"ok проверка подписки на тему {topic_id} запросом к gmun.pro/api, ")
                        return True
                    else:
                        if i == (devider-1):
                            self.pars_err(
                                f"## fail проверка подписки на тему {topic_id} "
                                f"ожидание {round((datetime.datetime.now() - t1).total_seconds())} сек.", noscreen=True)
                            return False
                    sleep(5)


            except Exception as e:
                self.pars_err(f"fail проверка подписки на тему, {e}", noscreen=True)

    def check_unsubscription(self, gid, uid, topic_id, fast=False, long=False):
        if self.inter_result["result"] != 1:
            try:
                t1 = datetime.datetime.now()
                if fast == True:
                    devider = 1
                else:
                    devider = 24

                for i in range(devider):
                    if not self.dev:
                        urlpart = 'gmun.pro'
                    else:
                        urlpart = 'gmun-php.dev.antipsy.ru'

                    url = f"https://{urlpart}/api/callback/vk/groups/get-users-by-topic-id?access_token=fGftE=lTXF]DeSnX5ztDm&gid={gid}&topic_id[]={topic_id}"
                    r = requests.request("GET", url)
                    a = r.status_code
                    b = str(r.content).strip('b\'[]')
                    if a == 200 and b.find(f"{uid}") == -1:
                        self.addcom("ok проверка отписки от темы")
                        return True
                    else:
                        if i == (devider-1):
                            if fast != True:
                                self.pars_err(
                                    f"## fail проверка отписки от темы {topic_id} запросом к gmun.pro/api, "
                                    f"ожидание {round((datetime.datetime.now() - t1).total_seconds())} сек.", noscreen=True)
                            return False
                    if long == True:
                        sleep(20)
                    else:
                        sleep(5)

            except Exception as e:
                self.pars_err(f"fail проверка отписки от темы, {e}", noscreen=True)

    def check_delivery(self, msg, gid, t_check):
        if self.inter_result["result"] != 1:
            with suppress(Exception):
                self.driver.get(f"https://vk.com/im?sel=-{gid}")
            sleep(1)
            datetime1 = datetime.datetime.now()
            devider = 15
            try:
                for i in range(round(t_check / devider)):
                    self.driver.refresh()
                    self.dwait(2)
                    with suppress(Exception):
                        self.find(".// *[contains(text(), 'Перейти в конец истории')]").click()
                        sleep(1)
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(1)
                    self.dwait(2)
                    if self.ifis_no_exception(f".//div[contains(text(), '{msg}')]") == True:
                        self.addcom(f"проверка доставки ок")
                        self.dwait(self.wait)
                        break
                    else:
                        sleep(devider-8)
                        if i == round((t_check / devider) - 1):
                            datetime2 = datetime.datetime.now()
                            delta = round(round((datetime1 - datetime2).total_seconds()))
                            self.dwait(self.wait)
                            self.pars_err(f"проверка доставки fail, сообщение с текстом {msg} не обнаружено в диалоге, время ожидания {delta} сек. ")
            except Exception as e:
                self.pars_err(f"исключение при проверке сообщения в диалоге, {e}")

    def get_frame(self):
            for i in range(2):
                sleep(1)
                if not self.dev:
                    self.gmun_frame = GMUN_IFRAME
                else:
                    self.gmun_frame = GMUN_IFRAME_DEV
                try:
                    self.driver.switch_to.frame(self.find(self.gmun_frame))
                    self.addcom(f"переход в iframe ok")
                    break
                except Exception:
                    if i == 1:
                        self.pars_err(f"переход в iframe fail")
                        raise
                    else:
                        pass


            #проверка отписки от всех тем

    def check_last_dialog_msg(self, gid, t_check):
        if self.inter_result["result"] != 1:
            with suppress(Exception):
                self.driver.get(f"https://vk.com/im?sel=-{gid}")
            datetime1 = datetime.datetime.now()
            try:
                devider = 10
                for i in range(round(t_check / devider)+3):
                    sleep(1)
                    self.driver.refresh()
                    self.dwait(3)
                    with suppress(Exception):
                        self.find(".// *[contains(text(), 'Перейти в конец истории')]").click()
                        sleep(1)
                    # sleep(1)
                    # self.dwait(2)
                    # self.driver.refresh()
                    # sleep(1)

                    xpath1 = f".//div[@class='im-mess-stack _im_mess_stack' or @class='im-mess-stack _im_mess_stack ' " \
                             f"and @data-peer='-{gid}'][last()]/descendant::*[@class='_im_mess_link'][last()]"

                    xpath2=f".//div[@class='im-mess-stack _im_mess_stack' or @class='im-mess-stack _im_mess_stack ' " \
                           f"and @data-peer='-{gid}'][last()]/descendant::*[@class='im-mess-stack--tools'][last()]"

                    if self.ifis_no_exception(xpath1):
                        msgtime = self.find(xpath1).get_attribute('text')
                    elif self.ifis_no_exception(xpath2):
                        msgtime = self.find(xpath2).text

                    tmsg = list(msgtime)
                    separator_index = tmsg.index(':')
                    tmp = str()
                    for j in range(separator_index):
                        tmp = tmp + tmsg[j]
                    hourmsg = int(tmp)
                    tmp = str()
                    j = separator_index + 1
                    while j < len(tmsg):
                        tmp = tmp + tmsg[j]
                        j = j + 1
                    minmsg = int(tmp)
                    datetime_msg = datetime.datetime(2000, 1, 1, hourmsg, minmsg, 0)
                    datetime_now = datetime.datetime.now().replace(year=2000, month=1, day=1, second=0, microsecond=0)
                    delta_min = round(abs((datetime_now - datetime_msg).total_seconds() / 60))
                    if delta_min <= t_check/60:
                        self.addcom(f'ok время сообщения в диалоге {str(datetime_msg)[11:16]}, ' \
                                    f'время проверки {str(datetime_now)[11:16]}')
                        self.dwait(self.wait)
                        break
                    else:
                        sleep(devider)
                        if abs(round((datetime1 - datetime.datetime.now()).total_seconds())) >= self.t_check:
                            datetime2 = datetime.datetime.now()
                            delta = abs(round((datetime1 - datetime2).total_seconds()))
                            self.dwait(self.wait)
                            self.pars_err(f'fail время сообщения в диалоге {str(datetime_msg)[11:16]}, ' \
                                          f'время проверки {str(datetime_now)[11:16]}, время ожидания {delta} секунд')
                            break
            except Exception as e:
                self.pars_err(f"исключение при проверке сообщения в диалоге, {e}")

    def check_last_dialog_msg_request(self, gid, token):
        if self.inter_result["result"] != 1:
            url = "https://api.vk.com/method/messages.getConversations"
            params = {
                'access_token': token,
                'group_id': gid,
                'v': 5.107,
                'count': 1
            }

            try:
                devider = 10
                for i in range(round(self.t_check / devider)):
                    r = requests.get(url, params=params, verify=False)
                    if r.status_code == 200 and r.json()['response']['items'][0]:
                        item = r.json()['response']['items'][0]
                        peer = item['conversation']['peer']['id']
                        out = item['last_message']['out']
                        datetime_msg = datetime.datetime.fromtimestamp(item['last_message']['date'])
                        datetime_now = datetime.datetime.now().replace(microsecond=0)
                        timedelta = abs(round((datetime_now - datetime_msg).total_seconds()))

                        if timedelta <= self.t_check and out == 1:
                            self.addcom(f"ok, время доставки сообщения {timedelta}, "
                                        f"время в диалоге {datetime_msg.strftime('%H:%M:%S')}, "
                                        f"время проверки {datetime_now.strftime('%H:%M:%S')}, лимит {self.t_check} сек.")
                            break
                        else:
                            if i == round(self.t_check / devider) - 1:
                                self.pars_err(f"fail, сообщение от сообщества не обнаружено за {self.t_check} сек.", noscreen=True)
                            sleep(devider)
                    else:
                        if i == round(self.t_check / devider) - 1:
                            self.pars_err(f"проверка сообщения от сценария запросом, status code {r.status_code}, {str(r.json())[:200]}", noscreen=True)
                        sleep(devider)

            except Exception as e:
                self.pars_err(f"fail, ошибка при проверке сообщения от сообщества запросом, \n{e}", noscreen=True)


    def send_to_vk_by_user_request(self, peer_id, token, message):
        if self.inter_result["result"] != 1:
            url = "https://api.vk.com/method/messages.send"
            params = {
                'access_token': token,
                'message' : message,
                'peer_id': peer_id, 'v': 5.102,
                'random_id':random.randint(1000,99999999)}
            try:
                r = requests.get(url, params=params, verify=False)
                if r.status_code != 200 or r.text.find("error_code") != -1:
                    self.pars_err(f"отправка стартового сообщения в диалог fail\nresponse.text: {r.text[:100]}", noscreen=True)
                else:
                    self.addcom(f"отправка стартового сообщения в диалог ok")
            except Exception as e:
                self.pars_err(str(e), noscreen=True)

    def send_to_vk_by_user_driver(self, gid, msg):
        if self.inter_result["result"] != 1:
            try:
                self.driver.get(f"https://vk.com/im?sel=-{gid}")
                self.dwait(7)
                self.supress_wait_8_sec(self.driver.find_element_by_xpath(".// *[contains(text(), 'Перейти в конец истории')]").click())
                self.find(".//*[contains(@id, 'im_editable')]").clear()
                self.find(".//*[contains(@id, 'im_editable')]").send_keys(f"{msg}")
                self.find(f".//*[@id='im_editable-{gid}']").send_keys(Keys.ENTER)
            except Exception as e:
                self.pars_err(f"исключение при отправке сообщения в диалог, {e}")

    def subscribe_by_driver(self, gid, topic_id):
        self.supress_wait_8_sec(self.driver.get(f"https://vk.com/app{self.app_id}_-{gid}#{topic_id}"))
        sleep(7)
        self.driver.refresh()
        sleep(4)
