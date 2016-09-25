# -*- encoding: utf-8 -*-

"""
Settings for dev environment.
"""

DEBUG = True

# Database
DATABASES = {
    'mysql': {
        'ENGINE': 'mysql',
        'NAME': 'redverntures',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': 3306,
        'CHARSET': 'utf8',
    },
    'rabbit': {
        'USER': 'guest',
        'PASSWORD': 'guest',
        'HOST': 'localhost',
        'PORT': 5672,
    }
}

# Tornado
TORNADO_SOCKETS = 15

# Celery Broker
CELERY_BROKER = 'amqp://{0}:{1}@{2}:{3}'.format(
    DATABASES["rabbit"]["USER"],
    DATABASES["rabbit"]["PASSWORD"],
    DATABASES["rabbit"]["HOST"],
    DATABASES["rabbit"]["PORT"]
)
