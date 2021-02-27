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
        GmunTest.__init__(self, name=self.name, no_driver=True)
        self.silent = silent or True
        self.wait = 60

    def test(self):
        msg = "@ss8545 test"
        self.mattermost.create_post(channel_test_fails, msg)




if __name__ == '__main__':
        print("started at ", time.strftime('%H:%M:%S').replace("'", ""))
        try:
            test_obj = Sender_Statuses().test()
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")


