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

nohup celery multi start  keyword_subscription -A gmun_tests.tests_alert.keyword_subscription worker -B -l info -c 2 --pidfile=tmp/pid_ks.pid -s tmp/schedule_ks -f tmp/log_ks -Q ks --without-gossip --without-mingle &
#--without-heartbeat