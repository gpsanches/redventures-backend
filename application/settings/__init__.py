# -*- encoding: utf-8 -*-

import os

# Environment
try:
    env = os.environ['APPLICATION_ENV']
except:
    env = 'dev'

# Imports settings
from application.settings.common import *
exec('from application.settings.{0} import *'.format(env))
