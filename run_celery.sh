#!/bin/sh
# wait for RabbitMQ server to start
celery -A mysite worker --concurrency=20
#cd mysite
## run Celery worker for our project mysite with Celery configuration stored in Celeryconf
## su -m myuser -c "celery worker -A mysite.celeryconf -Q default -n default@%h"
#
#su -m myuser -c "celery -A mysite worker --loglevel=info"
#celery -A mysite worker -B -E -l $debugLevel --concurrency=2 --autoreload