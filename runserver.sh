#!/usr/bin/env bash

pip install -r pip_requirements.txt
python manage.py runserver 0.0.0.0:808
celery -A mysite --port=5555 --broker=amqp://user:password@rabbit1:5672