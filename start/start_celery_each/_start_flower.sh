#!/bin/bash -x

cd $(pwd)/..
source venv/bin/activate
cd git
nohup celery flower --broker=redis://redis:cgfwtvh-ewr9syvh4-a8yhs@d05.antipsy.ru:6379/0 &
# --conf=gmun_tests/flowerconfig.py