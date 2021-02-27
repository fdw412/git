#!/bin/bash -x

cd /home/adminuser/autotests_2020_no_lxde
source venv/bin/activate
cd git
for ((i=0; i < 9999999; i++))
do
python3 -m gmun_tests.tests.ms_chain_action_subscr_unsubscr
python3 -m gmun_tests.tests.hashtag
python3 -m gmun_tests.tests.attachments
python3 -m gmun_tests.tests.ms_chain_read_check_positive
python3 -m gmun_tests.tests.ms_chain_membership
python3 -m gmun_tests.tests.ms_chain_gender_check
python3 -m gmun_tests.tests.ms_chain_name_check
python3 -m gmun_tests.tests.ms_chain_link_follow_check
python3 -m gmun_tests.tests.ms_chain_variables
python3 -m gmun_tests.tests.ms_chain_unsubscription_link
python3 -m gmun_tests.tests.interface
python3 -m gmun_tests.tests.gmun_bot
python3 -m gmun_tests.tests.add_app
python3 -m gmun_tests.tests.ms_chain_msg_delete
done