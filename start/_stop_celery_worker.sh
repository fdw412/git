#!/bin/bash -x

cd /home/adminuser/autotests_2020_no_lxde
source venv/bin/activate
cd git
nohup celery -A gmun_tests.tasks worker -B -l info &