import os, platform

if platform.system() == 'Windows':
    HEADLESS = 0
else:
    HEADLESS = 1

timedelta_sms_value = 60