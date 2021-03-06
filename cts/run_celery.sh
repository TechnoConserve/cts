#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

# run Celery worker for our project myproject with Celery configuration stored in celery.py
celery -A cts.celery worker -l INFO -Q default -n default@%h