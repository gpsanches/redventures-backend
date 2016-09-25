#!/bin/bash

root="/home/dev/unifiedplatform/python"
venv="/home/dev/env/bin/activate"

cd $root

#Cleans python cache
find . | egrep "*.pyc|__pycache__" | xargs rm -rf

# Set env variable
export APPLICATION_ENV=prod
export C_FORCE_ROOT="true"

# Start virtualenv
source $venv

# Kill current celery processes
killall -9 celery

# Workers
nohup celery -A celeryapp:celery_app worker -l DEBUG -c 1 -Q sample  > /tmp/celery_sample.log 2>&1 &

# Flower
#nohup celery flower -A celeryapp:celery_app --address=127.0.0.1 --port=5555
