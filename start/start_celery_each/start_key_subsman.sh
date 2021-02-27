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

nohup celery multi start  keyword_subscription_subsman -A gmun_tests.tests_alert.keyword_subscription_subsman worker -B -l info -c 2 --pidfile=tmp/pid_kss.pid -s tmp/schedule_kss -f tmp/log_kss -Q kss --without-gossip --without-mingle &
#--without-heartbeat