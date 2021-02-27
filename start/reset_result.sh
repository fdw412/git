#!/bin/bash -x

cd /home/adminuser/autotests_2020_no_lxde
source venv/bin/activate
cd git
python3 -m gmun_tests.utils.reset_result