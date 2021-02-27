#!/bin/bash -x

cd /home/adminuser/autotests_2020_no_lxde
source venv/bin/activate
cd git
for ((i=0; i < 9999999; i++)); do python3 -m gmun_tests.tests_alert.keyword_subscription_subsman; done