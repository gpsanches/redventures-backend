# -*- encoding: utf-8 -*-

import logging
import requests
from tornado.escape import json_decode
from application.src.celeryapp import CeleryApp, BaseTask
from application.src.utils import row2dict, list2dict
import application.settings as settings
from modules.widgetsspa.v1.settings import MODULE_NAME
from modules.widgetsspa.v1 import settings as users_settings
from modules.widgetsspa.v1.models import Users


# Logging handler
log = logging.getLogger(__name__)

# Celery App
celery = CeleryApp.get_instance(MODULE_NAME)

# filters search
ID_REQUEST = 'id'


class UserService(object):
    """
    Class is responsible to user service
    """

    @staticmethod
    def get_filters(filters, value):
        """
        Do the filter

        :param filters:
        :param value:
        :return: json, object
        """
        if filters == ID_REQUEST:
            json, users = UserService.get_by_id(value)
            return json, users

        else:
            json, users = UserService.get_all()
            return json, users

    @staticmethod
    def get_request_type(url):
        """
        verify the correctly filter in url request

        :param url:
        :return: None | string
        """
        if ID_REQUEST in url:
            return ID_REQUEST
        else:
            return None

    @staticmethod
    def get_all(deleted_at=None):
        """
        Return all data

        :param deleted_at:
        :return:json, object
        """
        users = UserService.get.db(users_settings.MODULE_NAME).query(Users).filter_by(deleted_at=deleted_at).all()
        json = list2dict(users, 'id') if users else None

        return json, users

    @staticmethod
    def get_by_id(id, deleted_at=None):
        """
        Return filter by id
        :param id:
        :param deleted_at:
        :return: json, object
        """
        users = UserService.get.db(users_settings.MODULE_NAME) \
            .query(Users).filter_by(id=id, deleted_at=deleted_at).first()
        json = row2dict(users) if users else None

        return json, users

    @staticmethod
    @celery.task(base=BaseTask, name="widgetsspa.v1.get")
    def get(url, data):
        """
        get database data

        :param url: string
        :param data: json
        :return: json | null
        :raise: Exception
        """
        try:
            json, users = UserService.get_filters(UserService.get_request_type(url), data['filter'])

            response = {
                "success": 1,
                "data": json
            }

            return response

        except Exception as e:
            log.error("The filter not found: "
                      "Body: {0} "
                      "Error: {1}. "
                      .format(data, e))

            response = {
                "success": 0,
                "data": data,
                "message": "The filter not found: {0}. ".format(data['filter'])
            }

            return response

    @staticmethod
    @celery.task(base=BaseTask, name="widgetsspa.v1.post")
    def post(self, transaction_uuid):
        """
        Method POST to API restful bundle

        :type transaction_uuid: string
        :param transaction_uuid: transaction uuid.

        :returns: json -- to sync requests (200) | empty string ("") -- to async requests (202).

        :raises: Exception (500)
        """
        try:
            is_sync = self.request.headers['is_sync']

            # Getting body + url data
            data = json_decode(self.request.body)
            data.update({"transaction_uuid": transaction_uuid})

            # Getting configs
            configs = self.service.get_configs(self.application.settings)

            if is_sync:
                # SYNC call
                response = self.service.post(self.request.uri, data, is_sync, configs)

                log.info("Bundle POST request successfully. "
                         "Request URL: {0}. "
                         "Request body: {1}. "
                         .format(self.request.uri, data))

                return self.success(response, 200)

            # Sending POST request to queued (async call)
            self.service.post.delay(self.request.uri, data, is_sync, configs)

            log.info("Bundle POST request successfully queued. "
                     "Request URL: {0}. "
                     "Request body: {1}. "
                     .format(self.request.uri, data))

            return self.success("", 202)

        except Exception as e:
            log.error("Bundle POST request error."
                      "Request URL: {0}. "
                      "Request body: {1}. "
                      "Exception: {2}. "
                      "Operation Hash: {3}."
                      .format(self.request.uri, self.request.body, e, LOG_HASH_POST))

            return self.error({
                "message": "Bundle POST request error."
                "Request URL: {0}. "
                "Request body: {1}. " . format(self.request.uri, self.request.body)
            }, 500)
