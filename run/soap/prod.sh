#!/bin/bash

root="/home/gpsanches/python/app/ui"
venv="source /home/gpsanches/python/env/ui/bin/activate"

###params
#$1 = port

cd $root

# Cleans python cache
find . | egrep "*.pyc|__pycache__" | xargs rm -rf

# Set env variable
export APPLICATION_ENV=prod

# Start virtualenv
source $venv

# Start server
killall -9 python
python api_soap.py $1
