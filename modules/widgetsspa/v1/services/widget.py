# -*- encoding: utf-8 -*-

import logging
import requests
from tornado.escape import json_decode
from application.src.celeryapp import CeleryApp, BaseTask
from application.src.utils import row2dict, list2dict
import application.settings as settings
from modules.widgetsspa.v1.settings import MODULE_NAME
from modules.widgetsspa.v1 import settings as widgets_settings
from modules.widgetsspa.v1.models import Widgets


# Logging handler
log = logging.getLogger(__name__)

# Celery App
celery = CeleryApp.get_instance(MODULE_NAME)

# filters search
ID_REQUEST = 'id'


class WidgetService(object):
    """
    Class is responsible to widget service
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
            json, widgets = WidgetService.get_by_id(value)
            return json, widgets

        else:
            json, widgets = WidgetService.get_all()
            return json, widgets

    @staticmethod
    def get_request_type(url):
        """
        verify what filter in url request

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
        widgets = WidgetService.get.db(widgets_settings.MODULE_NAME).query(Widgets).filter_by(deleted_at=deleted_at).all()
        json = list2dict(widgets, 'id') if widgets else None

        return json, widgets

    @staticmethod
    def get_by_id(id, deleted_at=None):
        """
        Return filter by id
        :param id:
        :param deleted_at:
        :return: json, object
        """
        widgets = WidgetService.get.db(widgets_settings.MODULE_NAME) \
            .query(Widgets).filter_by(id=id, deleted_at=deleted_at).first()
        json = row2dict(widgets) if widgets else None

        return json, widgets

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
            json, widgets = WidgetService.get_filters(WidgetService.get_request_type(url), data['filter'])

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
