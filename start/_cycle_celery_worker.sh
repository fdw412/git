#!/bin/bash -x

if [[ ! -d git ]]
then
    echo "no git dir, step up 1"
    cd ..

elif [[ ! -d git ]]
then
    echo "no git dir, step up 2"
    cd ../..

elif [[ ! -d git ]]
then
    echo "no git dir, step up 3"
    cd ../..

fi

ls -la


source venv/bin/activate
cd git
rm -rf tmp/* nohup.out start/nohup.out start/start_celery_each/nohup.out

#nohup celery flower --broker=redis://redis:cgfwtvh-ewr9syvh4-a8yhs@d05.antipsy.ru:6379/0 &
nohup celery multi start sender_receiver_status -A gmun_tests.tests_alert.sender_receiver_status worker -B -l info -c 1 --pidfile=tmp/pid_sender_receiver_status.pid -s tmp/schedule_sender_receiver_status -f tmp/log_sender_receiver_status -Q sender_receiver_status --without-gossip --without-mingle &
sleep 5
nohup celery multi start sender_front -A gmun_tests.tests_alert.sender_front worker -B -l info -c 1 --pidfile=tmp/pid_sender_front.pid -s tmp/schedule_sender_front -f tmp/log_sender_front -Q sender_front --without-gossip --without-mingle &
sleep 20
nohup celery multi start  keyword_subscription -A gmun_tests.tests_alert.keyword_subscription worker -B -l info -c 1 --pidfile=tmp/pid_keyword_subscription.pid -s tmp/schedule_keyword_subscription -f tmp/log_keyword_subscription -Q keyword_subscription --without-gossip --without-mingle &
sleep 20
nohup celery multi start ale_and_triggers -A gmun_tests.tests_alert.ale_and_triggers worker -B -l info -c 1 --pidfile=tmp/pid_ale_and_triggers.pid -s tmp/schedule_ale_and_triggers -f tmp/log_ale_and_triggers -Q ale_and_triggers --without-gossip --without-mingle &
sleep 20
nohup celery multi start non_alert -A gmun_tests.tasks worker -B -l info -c 1 --pidfile=tmp/pid_non_alert.pid -s tmp/schedule_non_alert -f tmp/log_non_alert -Q  non_alert --without-gossip --without-mingle &
sleep 20
nohup celery multi start sender_statuses -A gmun_tests.tests_alert.sender_statuses worker -B -l info -c 1 --pidfile=tmp/pid_sender_status.pid -s tmp/schedule_sender_statuses -f tmp/log_sender_statuses -Q sender_statuses --without-gossip --without-mingle &



#nohup celery multi start triggers -A gmun_tests.tests_alert.triggers worker -B -l info -c 1 --pidfile=tmp/pid_triggers.pid -s tmp/schedule_triggers -f tmp/log_triggers -Q triggers --without-gossip --without-mingle &
#sleep 20
#nohup celery multi start ale_msg_delayed -A gmun_tests.tests_alert.ale_msg_delayed worker -B -l info -c 1 --pidfile=tmp/pid_amd.pid -s tmp/schedule_amd -f tmp/log_amd -Q amd --without-gossip --without-mingle &
#sleep 20
#nohup celery multi start  keyword_subscription_subsman -A gmun_tests.tests_alert.keyword_subscription_subsman worker -B -l info -c 2 --pidfile=tmp/pid_kss.pid -s tmp/schedule_kss -f tmp/log_kss -Q kss --without-gossip --without-mingle &

#--without-heartbeat