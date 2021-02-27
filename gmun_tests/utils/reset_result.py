# -*- coding: utf-8 -*-

from gmun_tests import GmunTest
from gmun_tests.settings.test_run_params import test_run_params

import time
import json
no_driver = True
silent = True


for name in test_run_params:
    test_name = name
    run_series_count = test_run_params[name]['run_series_count']
    line=[]
    for j in range (run_series_count):
        line.append(f'0:{int(time.time())}')

    obj = GmunTest(no_driver)
    obj.redis.set(name, json.dumps(line))
    a = obj.redis.get(name)
    print(name," ", a.decode())

# name = 'Ale_Msg_Delayd'
# run_series_count = test_run_params[name]['run_series_count']
# line=[]
# for j in range (run_series_count):
#     line.append(f'1:{int(time.time())}')
#
# obj = GmunTest(no_driver)
# obj.redis.set(name, json.dumps(line))
# a = obj.redis.get(name)
# print(a.decode())

