# -*- encoding: utf-8 -*-

"""
Settings that is common to all environments: dev, homol and prod.
"""

import os
import logging.handlers
from datetime import timedelta
from celery.schedules import crontab


# Base dir of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Log Path
try:
    log_path = os.environ['APPLICATION_LOG_PATH']
except:
    log_path = "{0}/logs/application.log".format(BASE_DIR)

# Secret UUID to access internal URLs
INTERNAL_SECRET = 'd4959c4a-cc88-4f34-b5bb-22499d3006e4'

# Application settings
APPLICATION_TIMEOUT = 10
APPLICATION_ENCODING = 'utf-8'

# Active REST APIs
REST_MODULES = [
    'application',
    'modules.widgetsspa.v1.api.rest',
]

# Active Mock REST APIs
REST_MOCK_MODULES = [
    'modules.widgetsspa.v1.api.rest.mock',
]

# Active SOAP APIs
SOAP_MODULES = [

]

# Celery application name
CELERY_APP_NAME = 'widgetsspa'

# Celery Tasks (Async)
CELERY_TASKS = [
    'modules.widgetsspa.v1.services.sample',
]

# Celery Routes (Task vs Queue)
CELERY_ROUTES = {
    'application.request': {'queue': 'request'},
}

# Celery Schedule (Jobs)
CELERYBEAT_SCHEDULE = {

}

# Celery Default Configs
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

CELERY_RETRY = {
    'max_retries': 3,
    'default_retry_delay': 120,
}

CELERY_TIMEZONE = 'UTC'

CELERY_SERIALIZATION = 'yaml'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s'
        },
    },
    'loggers': {
        'root': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'application': {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': True,
        },
        'modules': {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': True,
        },
        'celery': {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': True,
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'NOTSET',
            'formatter': 'default',
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'default',
            'filename': "{0}/logs/application.log".format(BASE_DIR),
            'when': "D",
        },
    },
}
