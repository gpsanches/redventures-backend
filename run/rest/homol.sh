#!/bin/bash

root="/home/gpsanches/python/app/ui"
venv="source /home/gpsanches/python/env/ui/bin/activate"

###params
#$1 = port

cd $root

# Cleans python cache
find . | egrep "*.pyc|__pycache__" | xargs rm -rf

# Set env variable
export APPLICATION_ENV=homol

# Start virtualenv
source $venv

# Start server
killall -9 python
nohup python api_mock.py 8889 > /tmp/mock.log 2>&1 &
python api_rest.py $1
