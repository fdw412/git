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
from gmun_tests.settings import TOKEN_USER




gid = 190273847
uid=585675
topic_id = 623809
scenario = 51761

no_driver = True
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

    def test(self):
        test_start_time = datetime.datetime.now()
        try:
            self.inter_result = {'result': 0, 'results_line': [], 'results_line_datetime': [],
                                 'error': 'эмулиция ошибки', 'screen_paths':
                                     ['D:\\PycharmProjects\\git\\gmun_tests\\settings\\..\\screenshots\\___none.png',
                                      'D:\\PycharmProjects\\git\\gmun_tests\\settings\\..\\screenshots\\___none.png'],
                                 'comment': 'эмуляция ошибки'}
        except Exception as e:
            self.pars_err(f"fail ошибка добавления описания теста в словарь, {e}")

        self.test_ending()


if __name__ == '__main__':
    for i in range(1):
        print("started at ", time.strftime('%H:%M:%S').replace("'", ""))
        try:
            test_obj = Ale_Msg_Delayd().test()
        except Exception as e:
            print(f"ошибка выполнения __name__ = __main__, {e}")


