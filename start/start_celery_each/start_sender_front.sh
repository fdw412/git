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
rm -rf tmp/* nohup.out start/nohup.out start/start_celery_each/nohup.out

nohup celery multi start sender_front -A gmun_tests.tests_alert.sender_front worker -B -l info -c 2 --pidfile=tmp/pid_sf.pid -s tmp/schedule_sf -f tmp/log_sf -Q sf --without-gossip --without-mingle &
