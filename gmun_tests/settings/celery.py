import os, platform

REDIS_MASS_MAILING_THROTTLING_DB_NUMBER = 14
REDIS_SINGLE_MAILING_THROTTLING_DB_NUMBER = 15

# REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
# REDIS_HOST = 'd05.antipsy.ru'
# REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
# REDIS_PASSWORD = 'cgfwtvh-ewr9syvh4-a8yhs'


REDIS_HOST = '127.0.0.1'
REDIS_PASSWORD = ''

REDIS_PORT = os.environ.get('REDIS_PORT', '6379')


REDIS_DB_NUMBER = os.environ.get('REDIS_DB_NUMBER', 0)

REDIS_PASSWORD_URL_PART = REDIS_PASSWORD and f':{REDIS_PASSWORD}@' or ''

REDIS_DSN = (
    f'redis://{REDIS_PASSWORD_URL_PART}{REDIS_HOST}'
    f':{REDIS_PORT}/{REDIS_DB_NUMBER}'
)
CELERY_BROKER_URL = REDIS_DSN

# CELERY
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_SEND_TASK_ERROR_EMAILS = False
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_ENABLE_UTC = True
# CELERY_BROKER_URL = (
#     'redis://%s:%s/0' % (REDIS_HOST, REDIS_PORT)
# )

CELERY_TASK_IGNORE_RESULT = True
CELERY_DISABLE_RATE_LIMITS = True


CELERYD_HIJACK_ROOT_LOGGER = False
# CELERY_QUEUES = (
#     Queue('high', Exchange('high'), routing_key='high'),
#     Queue('normal', Exchange('normal'), routing_key='normal'),
#     Queue('low', Exchange('low'), routing_key='low'),
# )
CELERY_DEFAULT_QUEUE = 'normal'
CELERY_DEFAULT_EXCHANGE = 'normal'
CELERY_DEFAULT_ROUTING_KEY = 'normal'
CELERY_ROUTES = {
    # -- HIGH PRIORITY QUEUE -- #
    'myapp.tasks.check_payment_status': {'queue': 'high'},
    # -- LOW PRIORITY QUEUE -- #
    'myapp.tasks.close_session': {'queue': 'low'},
}
CELERY_BROKER = os.environ.get('CELERY_BROKER', 'redis://redis')
CELERY_IGNORE_RESULT = True
CELERYD_MAX_TASKS_PER_CHILD = 1
CELERYD_PREFETCH_MULTIPLIER = 1
