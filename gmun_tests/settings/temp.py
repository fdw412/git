from __future__ import absolute_import, unicode_literals
from celery import Celery
from gmun_tests.settings.celery import CELERY_BROKER_URL
app = Celery('gmun_tests', broker=CELERY_BROKER_URL)
from time import sleep
import random
from gmun_tests.settings.test_run_params import test_run_params

from gmun_tests.tests_alert.sender_front import Sender_Front
from gmun_tests.tests_alert.ale_msg_delayed import Ale_Msg_Delayd
from gmun_tests.tests_alert.keyword_subscription import Keyword_Subscription
from gmun_tests.tests_alert.keyword_subscription_subsman import Keyword_Subscription_Subsman
from gmun_tests.tests_alert.triggers import Triggers_Msg_Dialog
from gmun_tests.tests.ms_chain_action_subscr_unsubscr import Ms_Chain_Action_Subscr_Unsubscr
from gmun_tests.tests.hashtag import Hashtag
from gmun_tests.tests.attachments import Attachments
from gmun_tests.tests.ms_chain_read_check_positive import Ms_chain_action_read_check_positive
from gmun_tests.tests.ms_chain_membership import Ms_chain_membership
from gmun_tests.tests.ms_chain_gender_check import Ms_chain_gender_check
from gmun_tests.tests.ms_chain_name_check import Ms_chain_name_check
from gmun_tests.tests.ms_chain_link_follow_check import Ms_chain_link_follow_check
from gmun_tests.tests.ms_chain_variables import Ms_chain_variables
from gmun_tests.tests.ms_chain_unsubscription_link import Ms_chain_unsubscription_link
from gmun_tests.tests.interface import Interface
from gmun_tests.tests.add_app import Add_app



#@app.task(time_limit=400, name='task1')
#def test():
#        text=f'test1 {random.randint(0,100)}'
#        for i in range(0,4):
#            sleep(1)
#            print(text)

#@app.task(time_limit=400, name='task1')
#def test():
#        text=f'test1 {random.randint(0,100)}'
#        for i in range(0,4):
#            sleep(1)
#            print(text)

relative_delay=10

multi = 0
addon = 60
limit_sender_front = test_run_params['Sender_Front']['t_check'] + addon + relative_delay * multi
@app.task(time_limit=limit_sender_front, name='sender_front')
def sender_front():
    sleep(multi*relative_delay)
    Sender_Front().test(paused=False)

multi = 1
addon = 60
limit_ale_msg_delayed = test_run_params['Ale_Msg_Delayd']['t_check'] + addon + relative_delay * multi
@app.task(time_limit=limit_ale_msg_delayed, name='ale_msg_delayed')
def ale_msg_delayed():
    sleep(multi*relative_delay)
    Ale_Msg_Delayd().test(paused=False)

multi = 2
addon = 60
limit_keyword_subscription = test_run_params['Keyword_Subscription']['t_check'] + addon + relative_delay * multi
@app.task(time_limit=limit_keyword_subscription, name='keyword_subscription')
def keyword_subscription():
    sleep(multi*relative_delay)
    Keyword_Subscription().test(paused=False)

multi = 3
addon = 60
limit_keyword_subscription_subsman = test_run_params['Keyword_Subscription']['t_check'] + addon + relative_delay * multi
@app.task(time_limit=limit_keyword_subscription_subsman, name='keyword_subscription_subsman')
def keyword_subscription_subsman():
    sleep(multi*relative_delay)
    Keyword_Subscription_Subsman().test(paused=False)

multi = 4
addon = 60
limit_triggers = test_run_params['Triggers_Msg_Dialog']['t_check'] + addon + relative_delay * multi
@app.task(time_limit=limit_triggers, name='triggers')
def triggers():
    sleep(multi*relative_delay)
    Triggers_Msg_Dialog().test(paused=False)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(limit_sender_front + 5, sender_front.s(), name='sender_front')
    sender.add_periodic_task(limit_ale_msg_delayed+5, ale_msg_delayed.s(), name='ale_msg_delayed')
    sender.add_periodic_task(limit_keyword_subscription+5, keyword_subscription.s(), name='keyword_subscription')
    sender.add_periodic_task(limit_keyword_subscription_subsman+5, keyword_subscription_subsman.s(), name='keyword_subscription_subsman')
    sender.add_periodic_task(limit_triggers+5, triggers.s(), name='triggers')



# test.apply_async(retry=True)
#test2.apply_async(retry=True, countdown=10)

# чтобы заработало на виндовс
# pip install eventlet

# запуск воркера
# celery -A gmun_tests.tasks worker -l info -P eventlet
# celery -A gmun_tests.tasks worker -B -l info

#app.control.time_limit('gmun_tests.tasks.test', hard=6, reply=True)

# консоль
# запуск теста
# from gmun_tests.tasks import *
# test.apply_async(time_limit=5))
# test.apply_async()

#if __name__ == '__main__':
#     test().delay()
