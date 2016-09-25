# -*- encoding: utf-8 -*-

import logging
import requests
from tornado.escape import json_decode
from application.src.celeryapp import CeleryApp, BaseTask
import application.settings as settings
from modules.users.v1.settings import MODULE_NAME


# Logging handler
log = logging.getLogger(__name__)
LOG_HASH_SAMPLE = settings.LOG_HASHES[MODULE_NAME]["sample"]

# Celery App
celery = CeleryApp.get_instance()


class UserService(object):

    @staticmethod
    def get_configs(settings):
        """
        Returns useful configs.
        :param settings:
        :return: dict
        """
        return {
            'url': settings["config"]["users/v1/sample/url"],
            'file': settings["config"]["users/v1/sample/file"],
        }

    @staticmethod
    @celery.task(base=BaseTask, name="users.v1.sample.write_file")
    def write_file(phrase, configs):
        """
        Writes something into a file.
        :param phrase:
        :param configs:
        :return:
        """
        response = requests.get(url=configs["url"])
        body = json_decode(response.text)

        with open(configs["file"], 'w') as file:
            file.write("{0}: Parabéns pelos {1}. {2}.".format(body["name"], body["size"], phrase))
