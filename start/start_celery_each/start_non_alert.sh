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

nohup celery multi start non_alert -A gmun_tests.tasks worker -B -l info -c 1 --pidfile=tmp/pid_non_alert.pid -s tmp/schedule_non_alert -f tmp/log_non_alert -Q  non_alert --without-gossip --without-mingle &
#--without-heartbeat