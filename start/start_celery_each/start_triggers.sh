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
nohup celery multi start triggers -A gmun_tests.tests_alert.triggers worker -B -l info -c 2 --pidfile=tmp/pid_triggers.pid -s tmp/schedule_triggers -f tmp/log_triggers -Q triggers --without-gossip --without-mingle &
#--without-heartbeat