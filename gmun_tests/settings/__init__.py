import os
import datetime
import gmun_tests.debug_info
from logging import getLogger
from logging.config import dictConfig
from gmun_tests.debug_info import HEADLESS
import sentry_sdk
# from sentry_sdk.integrations.celery import CeleryIntegration



token_ms_chain_2020_gid_191083897 = "f9dee4193e4ddbeb67e9cef733e4adea4b3113b71a12a94c9d34e5d06b1f295dc708d1ee730138e5e2487"
token_triggers_gid_184517188 = "0121c37cb43d18d6e27f144d818bb3a4213dd7f3bf86557d69ce4ca878b767962349322e8d5cd54c924a9"

app_id_prod =  5728966
app_id_dev = 6347562
user_id = 585675
TOKEN_USER = 'ecd65c337d50675dcf9951445adb1b94ff307ea4e4b5e2d530a7e1194f7448d6792235b93541a7581e61e'
vk_user_login = 
vk_user_password = ""


SCREENSHOT_PATH = os.environ.get(
    'SCREENSHOT_PATH', os.sep.join([
        os.path.abspath(os.path.dirname(__file__)),
        '..',
        'screenshots',''
    ])
)
# SCREENSHOT_TIME_FORMAT = '%H_%M_%S'
SCREENSHOT_TIME_FORMAT = f'%d_%m_%H_%M_%S_mcsec_%f'

token = "EFA37D94-F152-3965-C80C-76DCF44352EC"

GMUN_IFRAME = (f".//iframe[contains(@src, 'gmun.pro/senderman')]")
GMUN_IFRAME_DEV = (f".//iframe[contains(@src, 'senderman.dev.antipsy')]")

CONSOLE_LOG_LEVEL = 'ERROR'
GRAYLOG_LOG_LEVEL = 'INFO'
LOGGER_FACILITY = 'gmun_tests'
LOGGER_BASE_NAME = 'gmun_tests'


SENTRY_DSN = ('https://1f466f1f8bb24db9b571386d637f9a6c:'
              '6c4b068378b340c39e0dca0cb21e5dd8@sentry.antipsy.ru/40')
SENTRY_URL = 'https://sentry.antipsy.ru'
SENTRY_API_TOKEN = '3ab4337523b8408f822bcedd07bb05a86b8ccdef50bb4a39b3d82dae5a55dc85'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'console': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s '
                      '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
            'datefmt': '%H:%M:%S',
        },
        'other': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s '
                      '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },

    'handlers': {
        'console': {
            'level': CONSOLE_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'stream': 'ext://sys.stdout',
        },
        'graypy': {
            'level': GRAYLOG_LOG_LEVEL,
            'class': 'graypy.GELFUDPHandler',
            'host': 'graylog.antipsy.ru',
            'port': 12201,
            'facility': LOGGER_FACILITY,
            'formatter': 'console',
        },
    },

    'loggers': {
        LOGGER_BASE_NAME: {
            'handlers': ['graypy', ],
            'level': 'INFO',
            'propagate': True,
        },
        'console': {
            'handlers': ['console', ],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
LOGGING = LOGGING_CONFIG

logger = getLogger(LOGGER_BASE_NAME)
dictConfig(LOGGING_CONFIG)

# if SENTRY_DSN:
#     sentry_sdk.init(
#         dsn=SENTRY_DSN,
#         integrations=[CeleryIntegration()],
#     )

PORTER_URL = 'http://porter.antipsy.ru/group_tokens/%s/'
PORTER_TOKEN = os.environ.get(
    'PORTER_TOKEN', 'fa58f2907adc088a38886c784ff1d28fd12ef17f')
SENDER_URL = 'https://sender.antipsy.ru/api/mailings/'
SENDER_TOKEN = os.environ.get(
    'SENDER_TOKEN', 'eda373fb132e90b3e2e207664678a1114ed7be21')
VK_API_VERSION = os.environ.get('VK_API_VERSION', 5.85)
MATTERMOST_URL = 'https://mattermost.antipsy.ru'
MATTERMOST_HOOK = '/hooks/husrt4z8w3r77nrks39rw18m7h'
MATTERMOST_CHANNEL = 'tests_logs'
# MATTERMOST_TOKEN = os.environ.get('MATTERMOST_TOKEN', '')
MATTERMOST_TOKEN = 'u3qyityngpgnznoh1xxy3f391o'

MATTERMOST_TEAM = 'developers'
ACK_MSG = 'Ja-Ja, achnowledge!'

DEFAULT_FAIL_PERCENT = 10
DEFAULT_FAIL_PERCENT_SMS = 30
DEFAULT_RUN_SERIES_COUNT = 10
DEFAULT_LAST_RESULT_COUNT = 3
DEFAULT_FAIL_LIMIT_COUNT = 2

# try:
#     from .settings_local import *  # noqa
# except ImportError:
#     import logging
#     logging.warn("There's no local settings file, running with stock settings")

