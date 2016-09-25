# -*- encoding: utf-8 -*-

from celery import Celery, Task
from application import settings
from application.src import databases
import logging
import logging.config


class CeleryApp:
    # Static property
    instance = {}

    @classmethod
    def get_instance(cls, module_name):
        """
        Returns Celery instance (singleton).
        :return: Celery
        """
        if module_name in cls.instance:
            return cls.instance[module_name]

        # Celery Broker
        celery_broker = 'amqp://{0}:{1}@{2}:{3}'.format(
            settings.DATABASES[module_name]["rabbitmq"]["USER"],
            settings.DATABASES[module_name]["rabbitmq"]["PASSWORD"],
            settings.DATABASES[module_name]["rabbitmq"]["HOST"],
            settings.DATABASES[module_name]["rabbitmq"]["PORT"]
        )

        # Celery App
        cls.instance[module_name] = Celery(
            "{0}_{1}".format(settings.CELERY_APP_NAME, module_name),
            broker=celery_broker,
            include=settings.CELERY_TASKS
        )

        # Celery Beat (Periodic Tasks)
        cls.instance[module_name].conf.CELERYBEAT_SCHEDULE = settings.CELERYBEAT_SCHEDULE

        # Routes
        cls.instance[module_name].conf.CELERY_ROUTES = settings.CELERY_ROUTES

        # Other settings
        cls.instance[module_name].conf.CELERY_ACCEPT_CONTENT = settings.CELERY_ACCEPT_CONTENT
        cls.instance[module_name].conf.CELERY_TIMEZONE = settings.CELERY_TIMEZONE
        cls.instance[module_name].conf.CELERY_RESULT_BACKEND = False
        cls.instance[module_name].conf.CELERY_IGNORE_RESULT = True
        cls.instance[module_name].conf.CELERY_SEND_EVENTS = False  # Will not create celeryev.* queues
        cls.instance[module_name].conf.CELERY_EVENT_QUEUE_EXPIRES = 60  # Will delete all celeryev. queues without consumers after 1 minute.
        cls.instance[module_name].conf.CELERY_TASK_SERIALIZER = 'json'
        cls.instance[module_name].conf.CELERY_MESSAGE_COMPRESSION = 'gzip'

        return cls.instance[module_name]


class BaseTask(Task):
    abstract = True
    _logger = None
    _db = {}
    _redis = {}
    _elastic = {}

    default_retry_delay = settings.CELERY_RETRY['default_retry_delay']
    max_retries = settings.CELERY_RETRY['max_retries']

    def db(self, module_name):
        if module_name not in self._db:
            mysql_configs = settings.DATABASES['application']["mysql-configs"]
            if "mysql-configs" in settings.DATABASES[module_name]:
                mysql_configs = settings.DATABASES[module_name]["mysql-configs"]

            self._db[module_name] = databases.DB().get_instance(
                name=module_name,
                data=settings.DATABASES[module_name]["mysql"],
                configs=mysql_configs
            )
        return self._db[module_name]

    @property
    def log(self):
        if not self._logger:
            try:
                logging.config.dictConfig(settings.LOGGING)
                self._logger = logging.getLogger("celery")
            except:
                pass
        return self._logger

    def redis(self, module_name):
        if module_name not in self._redis:
            self._redis[module_name] = databases.Redis().get_instance(
                name=module_name,
                connection=settings.DATABASES[module_name]["redis"]
            )
        return self._redis[module_name]

    def elastic(self, module_name):
        if module_name not in self._elastic:
            self._elastic[module_name] = databases.Elastic().get_instance(
                name=module_name
            )
        return self._redis[module_name]
