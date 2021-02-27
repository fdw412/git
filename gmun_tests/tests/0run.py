from gmun_tests.tests import attachments
from gmun_tests.tests import gmun_bot
from gmun_tests.tests import ms_chain_action_subscr_unsubscr
from gmun_tests.tests import ms_chain_read_check_positive
from gmun_tests.tests import ms_chain_membership
from gmun_tests.tests import hashtag
from gmun_tests.tests import ms_chain_gender_check
from gmun_tests.tests import ms_chain_name_check
from gmun_tests.tests import ms_chain_link_follow_check
from gmun_tests.tests import ms_chain_variables
from  gmun_tests.tests import  ms_chain_unsubscription_link
from  gmun_tests.tests import  interface

#
#
i=1
while 1:
    i+=1

    try:
        if i % 2 == 0:
            gid = 157361022
        if i % 2 == 1:
            gid = 161143917
        print(f"i {i}, gid {gid}")
        hashtag.Hashtag().test(gid = gid)
    except Exception as e:
      print(e)

    try:
        attachments.Attachments().test()
    except Exception as e:
        print(e)

    try:
        gmun_bot.Gmun_Bot().test()
    except Exception as e:
        print(e)

    try:
        ms_chain_action_subscr_unsubscr.Ms_Chain_Action_Subscr_Unsubscr().test()
    except Exception as e:
        print(e)

    try:
        ms_chain_read_check_positive.Ms_chain_action_read_check_positive().test()
    except Exception as e:
       print(e)

    try:
        ms_chain_membership.Ms_chain_membership().test()
    except Exception as e:
       print(e)

    try:
        ms_chain_gender_check.Ms_chain_gender_check().test()
    except Exception as e:
       print(e)

    try:
        ms_chain_name_check.Ms_chain_name_check().test()
    except Exception as e:
       print(e)

    try:
       ms_chain_link_follow_check.Ms_chain_link_follow_check().test()
    except Exception as e:
       print(e)

    try:
        ms_chain_variables.Ms_chain_variables().test()
    except Exception as e:
        print(e)

    try:
        ms_chain_unsubscription_link.Ms_chain_unsubscription_link().test()
    except Exception as e:
        print(e)

    try:
        interface.Interface().test()
    except Exception as e:
        print(e)