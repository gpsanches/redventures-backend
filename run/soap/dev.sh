#!/bin/bash

root="/home/gpsanches/python/app/ui"
venv="source /home/gpsanches/python/env/ui/bin/activate"


cd $root

# Cleans python cache
find . | egrep "*.pyc|__pycache__" | xargs rm -rf

# Set env variable
export APPLICATION_ENV=dev

# Start virtualenv
source $venv

# Start server
killall -9 python
python api_soap.py 8888
