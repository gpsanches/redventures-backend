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
from sqlalchemy.exc import IntegrityError


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
    def add(session, user):
        """
        Save the user

        :param session:
        :param user:
        :return: json, object
        """

        user_object = Users(
            name=user["name"],
            gravatar=user["gravatar"]
        )

        session.add(user_object)
        session.flush()
        session.refresh(user_object)
        user.update({"id": user_object.id})

        return user, user_object

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
        users = UserService.get.db(users_settings.MODULE_NAME).query(Users).all()
        json = list2dict(users, 'id') if users else None

        return json, users

    @staticmethod
    def get_by_id(id):
        """
        Return filter by id
        :param id:
        :return: json, object
        """
        users = UserService.get.db(users_settings.MODULE_NAME) \
            .query(Users).filter_by(id=id).first()
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
    def post(url, data):
        """
        Sync or async save bundle database data

        :param url: string
        :param data: json
        :param is_sync: boolean
        :param configs: dict
        :return: json | null
        :raises: IntegrityError, Exception
        """
        task = UserService.post
        try:
            json, object = UserService.add(task.db(users_settings.MODULE_NAME), data)

            response = {
                "success": 1,
                "data": json
            }

            # log
            task.log.info(response)

            return response

        except IntegrityError as ie:
            task.log.error("This User already exists! "
                           "Body: {0} "
                           "Error: {1}. "
                           .format(url, data, ie))

            response = {
                "success": 0,
                "data": data,
                "message": "This user already exists! "
            }

            return response

        except Exception as e:
            task.log.error("Could not create user. "
                           "Body: {0} "
                           "Error: {1}. "
                           .format(data, e))

            response = {
                "success": 0,
                "message": "Could not create user.",
                "data": data
            }

            return response
