FROM python:2.7.12
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

#ENTRYPOINT celery -A mysite worker --concurrency=20 --loglevel=info