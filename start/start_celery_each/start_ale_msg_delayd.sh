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
source venv/bin/activate
cd git

nohup celery multi start ale_msg_delayd -A gmun_tests.tests_alert.ale_msg_delayed worker -B -l info -c 2 --pidfile=tmp/pid_amd.pid -s tmp/schedule_amd -f tmp/log_amd -Q amd --without-gossip --without-mingle &
#--without-heartbeat