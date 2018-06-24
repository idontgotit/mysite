#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

cd mysite
# run Celery worker for our project mysite with Celery configuration stored in Celeryconf
# su -m myuser -c "celery worker -A mysite.celeryconf -Q default -n default@%h"

su -m myuser -c "celery -A mysite worker --loglevel=info"