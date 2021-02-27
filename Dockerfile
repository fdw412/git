FROM python:3.6-slim-buster
ENV TZ Europe/Moscow

RUN apt update && apt install -y mc htop procps
WORKDIR /usr/git/
COPY chrome80.deb chromedriver pip requirements.txt /usr/git/

RUN chmod +x ./chromedriver
RUN chmod +x ./chrome80.deb
RUN apt install -y $PWD/chrome80.deb
WORKDIR /usr/
RUN pip install virtualenv
RUN virtualenv venv
RUN . venv/bin/activate
RUN pip install --upgrade pip
WORKDIR /usr/git/
RUN pip install -r requirements.txt

#RUN pip install -U Celery
#CMD bash start/start_celery_each/sender_front.sh
#RUN bash _cycle_celery_worker.sh
#CMD python3 -m gmun_tests.tests_alert.sender_front -paused False
