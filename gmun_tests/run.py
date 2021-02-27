from celery import Celery
from gmun_tests.tasks import sender_front

sender_front.delay()