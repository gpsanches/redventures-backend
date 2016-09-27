#!/bin/bash

root="/Users/gsanches/Projects/python/redventures"
venv="source /Users/gsanches/Projects/python/env/redventures/bin/activate"

cd $root

# Cleans python cache
find . | egrep "*.pyc|__pycache__" | xargs rm -rf

# Set env variable
export APPLICATION_ENV=dev

# Start virtualenv
source $venv

# Start server
killall -9 python

# nohup python api_mock.py 8889 > /tmp/mock.log 2>&1 &
python api_rest.py 8888
