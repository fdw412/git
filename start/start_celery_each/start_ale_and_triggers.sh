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
nohup celery multi start ale_and_triggers -A gmun_tests.tests_alert.ale_and_triggers worker -B -l info -c 2 --pidfile=tmp/pid_ale_and_triggers.pid -s tmp/schedule_ale_and_triggers -f tmp/log_ale_and_triggers -Q ale_and_triggers --without-gossip --without-mingle &
#--without-heartbeat