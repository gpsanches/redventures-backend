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
from sqlalchemy.exc import IntegrityError


# Logging handler
log = logging.getLogger(__name__)

# Celery App
celery = CeleryApp.get_instance(MODULE_NAME)

# filters search
ID_REQUEST = 'id'
NAME_REQUEST = 'name'


class WidgetService(object):
    """
    Class is responsible to widget service
    """

    @staticmethod
    def add(session, user):
        """
        Save the widget

        :param session:
        :param user:
        :return: json, object
        """

        user_object = Widgets(
            name=user["name"],
            color=user["color"],
            price=user["price"],
            inventory=user["inventory"],
            melts=user["melts"],
        )

        session.add(user_object)
        session.flush()
        session.refresh(user_object)
        user.update({"id": user_object.id})

        return user, user_object

    @staticmethod
    def update(session, obj, widget):
        """
        Update widget data

        :param session:
        :param obj:
        :param widget:
        :return: object

        :raises Exception
        """
        if not WidgetService.get_by_id(widget["id"]):
            raise Exception("The widget id not found with uuid {0}.".format(widget["id"]))

        obj.name = widget["name"] if "name" in widget else obj.name
        obj.color = widget["color"] if "color" in widget else obj.color
        obj.price = widget["price"] if "price" in widget else obj.price
        obj.inventory = widget["inventory"] if "inventory" in widget else obj.inventory
        obj.melts = widget["melts"] if "melts" in widget else obj.melts

        session.flush()

        return widget

    @staticmethod
    def remove(session, obj, widget):
        """
        delete data

        :param session:
        :param obj:
        :param widget:
        :return: object
        """

        session.delete(obj)
        session.flush()

        return widget

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

        elif filters == NAME_REQUEST:
            json, widgets = WidgetService.get_by_name(value)
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
        if "{0}{1}{2}".format("/", ID_REQUEST, "/") in url:
            return ID_REQUEST
        elif NAME_REQUEST in url:
            return NAME_REQUEST
        else:
            return None

    @staticmethod
    def get_all():
        """
        Return all data
        :return:json, object
        """
        widgets = WidgetService.get.db(widgets_settings.MODULE_NAME).query(Widgets).all()
        json = list2dict(widgets, 'id') if widgets else None

        return json, widgets

    @staticmethod
    def get_by_id(id):
        """
        Return filter by id
        :param id:
        :return: json, object
        """
        widgets = WidgetService.get.db(widgets_settings.MODULE_NAME) \
            .query(Widgets).filter_by(id=id).first()
        json = row2dict(widgets) if widgets else None

        return json, widgets

    @staticmethod
    def get_by_name(name):
        """
        Return filter by name
        :param id:
        :return: json, object
        """
        widgets = WidgetService.get.db(widgets_settings.MODULE_NAME) \
            .query(Widgets).filter_by(name=name).first()
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

    @staticmethod
    @celery.task(base=BaseTask, name="widgetsspa.v1.post")
    def post(url, data):
        """
        Save widgets database data

        :param url: string
        :param data: json
        :return: json | null
        :raises: IntegrityError, Exception
        """
        task = WidgetService.post
        try:
            json, object = WidgetService.add(task.db(widgets_settings.MODULE_NAME), data)

            response = {
                "success": 1,
                "data": json
            }

            # log
            task.log.info(response)

            return response

        except IntegrityError as ie:
            task.log.error("This Widget already exists! "
                           "Body: {0} "
                           "Error: {1}. "
                           .format(url, data, ie))

            response = {
                "success": 0,
                "data": data,
                "message": "This widget already exists! "
            }

            return response

        except Exception as e:
            task.log.error("Could not create widget. "
                           "Body: {0} "
                           "Error: {1}. "
                           .format(data, e))

            response = {
                "success": 0,
                "message": "Could not create widget.",
                "data": data
            }

            return response

    @staticmethod
    @celery.task(base=BaseTask, name="widgetsspa.v1.put")
    def put(url, data):
        """
        update widget database widget

        :param url: string
        :param data: json

        :return: json | null
        :raises: IntegrityError, Exception
        """
        task = WidgetService.put
        try:
            json, widget = WidgetService.get_by_id(data['id'])

            if not widget:
                task.log.error("The widget id could not be found to update. "
                               "Url origin: {0} "
                               "Body: {1} "
                               .format(url, data))

                response = {
                    "success": 0,
                    "message": "The widget id {0} could not be found to update.".format(data['id']),
                    "data": data
                }
                return response

            json = WidgetService.update(task.db(widgets_settings.MODULE_NAME), widget, data)
            message = "Widget updated successfully! Url origin: {0} body: {1}".format(url, data)
            task.log.info(message)

            response = {
                "success": 1,
                "data": json
            }
            return response

        except IntegrityError as ie:
            task.log.error("This Widget already exists! "
                           "Url origin: {0} "
                           "Body: {1} "
                           "Error: {2}. "
                           .format(url, data, ie))

            response = {
                "success": 0,
                "url destiny": url,
                "data": data,
                "message": "This Widget already exists!"
            }

            return response

        except Exception as e:
            task.log.error("Could not update Widget {0}. "
                           "Error: {1}. "
                           .format(data, e))

            message = "Could not update Widget {0}. Error: {1}.".format(data, e)

            response = {
                "success": 0,
                "data": data,
                "message": message
            }

            return response

    @staticmethod
    @celery.task(base=BaseTask, name="widgetsspa.v1.delete")
    def delete(url, data):
        """
        delete data in widget table

        :param url: string
        :param data: json
        :return: json | null
        :raise: Exception
        """
        task = WidgetService.delete
        try:
            json, widget = WidgetService.get_by_id(data['id'])

            if not widget:
                task.log.error("The widget id could not be found to delete. "
                               "Body: {0} "
                               .format(url, data))

                response = {
                    "success": 0,
                    "data": data,
                    "message": "The widget id {0} could not be found to delete. ".format(data['id'])
                }
                return response

            message = "The widget id {0} was deleted. {1}. ".format(data['id'], data)
            data = WidgetService.remove(task.db(widgets_settings.MODULE_NAME), widget, data)
            task.log.info(message)

            response = {
                "success": 1,
                "data": data
            }
            return response

        except Exception as e:
            task.log.error("The widget id could not be found to delete. {0} "
                           "Error: {1}. "
                           .format(data, e))

            message = "The widget_uuid could not be found to delete. {0} " \
                      "Error: {1}".format(data, e)

            response = {
                "success": 0,
                "data": data,
                "message": message
            }

            return response
