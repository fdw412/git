from __future__ import absolute_import, unicode_literals
from celery import Celery
from gmun_tests.settings.celery import CELERY_BROKER_URL
app = Celery('gmun_tests', broker=CELERY_BROKER_URL)
from time import sleep
import random
from celery.exceptions import SoftTimeLimitExceeded
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from gmun_tests.utils.mattermost import Mattermost

# from gmun_tests.tests_alert.sender_front import Sender_Front
# from gmun_tests.tests_alert.ale_msg_delayed import Ale_Msg_Delayd
# from gmun_tests.tests_alert.keyword_subscription import Keyword_Subscription
from gmun_tests.tests_alert.keyword_subscription_subsman import Keyword_Subscription_Subsman
# from gmun_tests.tests_alert.triggers import Triggers_Msg_Dialog
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
# from gmun_tests.tests_alert.sender_statuses import Sender_Statuses
#
# @app.task(soft_time_limit=400, time_limit=410, name='sender_front')
# def sender_front():
#     try:
#         Sender_Front().test(paused=False)
#     except SoftTimeLimitExceeded:
#         Mattermost().celery_exception_send("sender_front")
#
# @app.task(soft_time_limit=400, time_limit=410, name='ale_msg_delayed')
# def ale_msg_delayed():
#     try:
#         Ale_Msg_Delayd().test(paused=False)
#     except SoftTimeLimitExceeded:
#         Mattermost().celery_exception_send("ale_msg_delayed")
#
# @app.task(soft_time_limit=400, time_limit=410, name='keyword_subscription')
# def keyword_subscription():
#     try:
#         Keyword_Subscription().test(paused=False)
#     except SoftTimeLimitExceeded:
#         Mattermost().celery_exception_send("keyword_subscription")
#
# @app.task(soft_time_limit=400, time_limit=410, name='keyword_subscription_subsman')
# def keyword_subscription_subsman():
#     try:
#         Keyword_Subscription_Subsman().test(paused=False)
#     except SoftTimeLimitExceeded:
#         Mattermost().celery_exception_send("keyword_subscription_subsman")
#
# @app.task(soft_time_limit=400, time_limit=410, name='triggers')
# def triggers():
#     try:
#         Triggers_Msg_Dialog().test(paused=False)
#     except SoftTimeLimitExceeded:
#         Mattermost().celery_exception_send("triggers")

@app.task(soft_time_limit=900, time_limit=910, name='ms_chain_action_subscr_unsubscr')
def ms_chain_action_subscr_unsubscr():
    try:
        Ms_Chain_Action_Subscr_Unsubscr().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"ms_chain_action_subscr_unsubscr, {e}")

@app.task(soft_time_limit=900, time_limit=910, name='hashtag')
def hashtag():
    try:
        Hashtag().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"hashtag, {e}")


@app.task(soft_time_limit=900, time_limit=910, name='attachments')
def attachments():
    try:
        Attachments().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"attachments, {e}")


@app.task(soft_time_limit=900, time_limit=910, name='ms_chain_read_check_positive')
def ms_chain_read_check_positive():
    try:
        Ms_chain_action_read_check_positive().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"ms_chain_read_check_positive, {e}")


@app.task(soft_time_limit=900, time_limit=910, name='ms_chain_membership')
def ms_chain_membership():
    try:
        Ms_chain_membership().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"ms_chain_membership, {e}")


@app.task(soft_time_limit=900, time_limit=910, name='ms_chain_gender_check')
def ms_chain_gender_check():
    try:
        Ms_chain_gender_check().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"ms_chain_gender_check, {e}")


@app.task(soft_time_limit=900, time_limit=910, name='ms_chain_name_check')
def ms_chain_name_check():
    try:
        Ms_chain_name_check().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"ms_chain_name_check, {e}")


@app.task(soft_time_limit=900, time_limit=910, name='ms_chain_link_follow_check')
def ms_chain_link_follow_check():
    try:
        Ms_chain_link_follow_check().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"ms_chain_link_follow_check, {e}")


@app.task(soft_time_limit=900, time_limit=910, name='ms_chain_variables')
def ms_chain_variables():
    try:
        Ms_chain_variables().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"ms_chain_variables, {e}")


@app.task(soft_time_limit=900, time_limit=910, name='ms_chain_unsubscription_link')
def ms_chain_unsubscription_link():
    try:
        Ms_chain_unsubscription_link().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"ms_chain_unsubscription_link, {e}")


@app.task(soft_time_limit=1200, time_limit=1210, name='interface')
def interface():
    try:
        Interface().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"interface, {e}")


@app.task(soft_time_limit=1200, time_limit=1210, name='add_app')
def add_app():
    try:
        Add_app().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"add_app, {e}")

@app.task(soft_time_limit=400, time_limit=410, name='keyword_subscription_subsman')
def keyword_subscription_subsman():
    try:
        Keyword_Subscription_Subsman().test(paused=False)
    except Exception as e:
        Mattermost().celery_exception_send(f"keyword_subscription_subsman, {e}")

app.control.purge()

# app.add_periodic_task(420, sender_front.s(), name='sender_front')
# app.add_periodic_task(420, ale_msg_delayed.s().set(countdown=20), name='ale_msg_delayed')
# app.add_periodic_task(420, keyword_subscription.s().set(countdown=30), name='keyword_subscription')
# app.add_periodic_task(420, keyword_subscription_subsman.s().set(countdown=40), name='keyword_subscription_subsman')
# app.add_periodic_task(420, triggers.s().set(countdown=50), name='triggers')
# app.add_periodic_task(1220, ms_chain_action_subscr_unsubscr.s(), name='ms_chain_action_subscr_unsubscr')
# app.add_periodic_task(1000, hashtag.s(), name='hashtag')
# app.add_periodic_task(1000, attachments.s(), name='attachments')
# app.add_periodic_task(1000, ms_chain_read_check_positive.s(), name='ms_chain_read_check_positive')
# app.add_periodic_task(1000, ms_chain_membership.s(), name='ms_chain_membership')
# app.add_periodic_task(1000, ms_chain_gender_check.s(), name='ms_chain_gender_check')
# app.add_periodic_task(1000, ms_chain_name_check.s(), name='ms_chain_name_check')
# app.add_periodic_task(1000, ms_chain_variables.s(), name='ms_chain_variables')
# app.add_periodic_task(1000, ms_chain_unsubscription_link.s(), name='ms_chain_unsubscription_link')
# app.add_periodic_task(2000, interface.s(), name='interface')
# app.add_periodic_task(1000+60*60*24, add_app.s(), name='add_app')

app.conf.beat_schedule = {
'ms_chain_action_subscr_unsubscr': {'task': 'ms_chain_action_subscr_unsubscr','schedule': 1220, 'options': {'queue': 'non_alert'}},
'hashtag': {'task': 'hashtag','schedule': 1800, 'options': {'queue': 'non_alert'}},
'attachments': {'task': 'attachments','schedule': 1000, 'options': {'queue': 'non_alert'}},
'ms_chain_read_check_positive': {'task': 'ms_chain_read_check_positive','schedule': 1000, 'options': {'queue': 'non_alert'}},
'ms_chain_membership': {'task': 'ms_chain_membership','schedule': 1000, 'options': {'queue': 'non_alert'}},
'ms_chain_gender_check': {'task': 'ms_chain_gender_check','schedule': 1000, 'options': {'queue': 'non_alert'}},
'ms_chain_name_check': {'task': 'ms_chain_name_check','schedule': 1000, 'options': {'queue': 'non_alert'}},
'ms_chain_unsubscription_link': {'task': 'ms_chain_unsubscription_link','schedule': 1000, 'options': {'queue': 'non_alert'}},
'interface': {'task': 'interface','schedule': 2000, 'options': {'queue': 'non_alert'}},
'add_app': {'task': 'add_app','schedule': 1000+60*60*24, 'options': {'queue': 'non_alert'}},
'keyword_subscription_subsman': {'task': 'keyword_subscription_subsman','schedule': 420, 'options': {'queue': 'non_alert'}}
}

# чтобы заработало на виндовс
# pip install eventlet

# запуск воркера
# celery -A gmun_tests.tasks worker -l info -P eventlet
# celery -A gmun_tests.tasks worker -B -l info --autoscale=40,1

# celery multi start w1 -A gmun_tests.tasks worker -B -l info --autoscale=40,1
# посмотреть через htop имена процессов, если нельзя более точные, то pkill -9 -f 'celery'

# сначала регистрируем таск

# celery -A gmun_tests.tests_alert.sender_front worker -B -l INFO --concurrency=2 -n worker1234567890@%%h
# celery multi start 2 -A gmun_tests.tests_alert.ale_msg_delayed worker -B -l info --autoscale=3,1 --pidfile=celery_ale_msg_delayed_beat.pid -s schedule_ale_msg_delayed -f celery_log_ale_msg_delayed
# celery -A gmun_tests.tasks worker -B -l info -c 10 --pidfile=tmp/alert.pid -s tmp/alert_schedule -Q alert -n alert@%%h
# celery -A gmun_tests.tasks worker -B -l info -c 1 --pidfile=tmp/non_alert.pid -s tmp/non_alert_schedule -Q alert -n non_alert@%%h
# celery multi start alert -A gmun_tests.tasks worker -B -l info -c 10 --pidfile=tmp/alert.pid -s tmp/alert_schedule -f tmp/alert_log -Q alert
# celery multi start non_alert -A gmun_tests.tasks worker -B -l info -c 1 --pidfile=tmp/non_alert.pid -s tmp/non_alert_schedule -f tmp/non_alert_log -Q non_alert
#

# celery -A gmun_tests.tests_alert.sender_front worker -B -l info -c 1 --pidfile=tmp/pid_sender_front.pid -s tmp/schedule_sender_front -f tmp/log_sender_front -Q sender_front -n worker_sender_front
# celery -A gmun_tests.tests_alert.ale_msg_delayed worker -B -l info -c 1 --pidfile=tmp/pid_ale_msg_delayed.pid -s tmp/schedule_ale_msg_delayed -f tmp/log_ale_msg_delayed -Q ale_msg_delayed -n worker_ale_msg_delayed
# celery -A gmun_tests.tests_alert.keyword_subscription worker -B -l info -c 1 --pidfile=tmp/pid_keyword_subscription.pid -s tmp/schedule_keyword_subscription -f tmp/log_keyword_subscription -Q keyword_subscription -n worker_keyword_subscription
# celery -A gmun_tests.tests_alert.keyword_subscription_subsman worker -B -l info -c 1 --pidfile=tmp/pid_keyword_subscription_subsman.pid -s tmp/schedule_keyword_subscription_subsman -f tmp/log_keyword_subscription_subsman -Q keyword_subscription_subsman -n worker_keyword_subscription_subsman
# celery -A gmun_tests.tests_alert.triggers worker -B -l info -c 1 --pidfile=tmp/pid_triggers.pid -s tmp/schedule_triggers -f tmp/log_triggers -Q triggers -n worker_triggers
# celery -A gmun_tests.tests_alert.tasks worker -B -l info -c 1 --pidfile=tmp/pid_non_alert.pid -s tmp/schedule_non_alert -f tmp/log_non_alert -Q non_alert -n non_alert

# celery multi start worker_sf -A gmun_tests.tests_alert.sender_front worker -B -l info -c 1 --pidfile=tmp/pid_sf.pid -s tmp/schedule_sf -f tmp/log_sf -Q sf
# celery multi start worker_amd -A gmun_tests.tests_alert.ale_msg_delayed worker -B -l info -c 1 --pidfile=tmp/pid_amd.pid -s tmp/schedule_amd -f tmp/log_amd -Q amd
# celery multi start  worker_ks -A gmun_tests.tests_alert.keyword_subscription worker -B -l info -c 1 --pidfile=tmp/pid_ks.pid -s tmp/schedule_ks -f tmp/log_ks -Q ks
# celery multi start  worker_kss -A gmun_tests.tests_alert.keyword_subscription_subsman worker -B -l info -c 1 --pidfile=tmp/pid_kss.pid -s tmp/schedule_kss -f tmp/log_kss -Q kss
# celery multi start worker_triggers -A gmun_tests.tests_alert.triggers worker -B -l info -c 1 --pidfile=tmp/pid_triggers.pid -s tmp/schedule_triggers -f tmp/log_triggers -Q triggers
# celery multi start worker_non_alert -A gmun_tests.tasks worker -B -l info -c 1 --pidfile=tmp/pid_non_alert.pid -s tmp/schedule_non_alert -f tmp/log_non_alert -Q kss

# celery flower --broker=redis://redis:cgfwtvh-ewr9syvh4-a8yhs@d05.antipsy.ru:6379/0

# консоль
# запуск теста
# from gmun_tests.tasks import *
# test.apply_async(time_limit=5))
# test.apply_async()
#
# if __name__ == '__main__':
#     send("test")
