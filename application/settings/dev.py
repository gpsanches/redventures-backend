# -*- encoding: utf-8 -*-

"""
Settings for dev environment.
"""

DEBUG = True

# Database
DATABASES = {
    # Application
    "application": {
        'mysql-configs': {
            'pool_recycle': 3600,
            'pool_size': 5,
            'max_overflow': 10,
            'timeout': 30
        },
        'rabbit': {
            'USER': 'guest',
            'PASSWORD': 'guest',
            'HOST': 'localhost',
            'PORT': 5672,
        },
    },
    # widgetsspa
    "widgetsspa": {
        'mysql': {
            'ENGINE': 'mysql',
            'NAME': 'redventures',
            'USER': 'root',
            'PASSWORD': '123456',
            'HOST': '127.0.0.1',
            'PORT': 3306,
            'CHARSET': 'utf8',
        },
        'rabbitmq': {
            'USER': 'guest',
            'PASSWORD': 'guest',
            'HOST': 'localhost',
            'PORT': 5672,
        },
    },
}

# Tornado
TORNADO_SOCKETS = 1

# Celery Broker
CELERY_BROKER = 'amqp://{0}:{1}@{2}:{3}'.format(
    DATABASES["application"]["rabbit"]["USER"],
    DATABASES["application"]["rabbit"]["PASSWORD"],
    DATABASES["application"]["rabbit"]["HOST"],
    DATABASES["application"]["rabbit"]["PORT"]
)
