# -*- encoding: utf-8 -*-

import logging
from tornado.escape import json_decode
import application.settings as settings
from application.src.rewrites import APIHandler
from modules.widgetsspa.v1.services import widget as services
from modules.widgetsspa.v1.validators import widget as validate
from modules.widgetsspa.v1.settings import MODULE_NAME, MODULE_VERSION


# Logging
log = logging.getLogger(__name__)


class WidgetHandler(APIHandler):

    __urls__ = [
        # get
        r"/widgets(?:/)?",

        # get or post with id
        r"/widgets/id/([0-9]+)(?:/)?",

        # get by name
        r"/widgets/name/([a-zA-Z\-0-9\.:,_]+)(?:/)?",
    ]

    # Service
    service = services.WidgetService()

    @validate.get
    def get(self, filter=None):
        """
        Receives POST requests.
        :return:
        """
        try:
            # Getting url
            data = {"filter": filter}

            response = self.service.get(self.request.uri, data)

            log.info("Widget GET request successfully. ")

            return self.success(response, 200)

        except Exception as e:
            log.error("Widget GET request Error."
                      "Exception: {0}. "
                      .format(e))

            return self.error({"success": 0, "message": "GET request Error!"}, 500)

    @validate.post
    def post(self):
        """
        Method POST to API restful widget

        :returns: json -- to sync requests (200) | empty string ("").

        :raises: Exception (500)
        """
        try:

            # Getting body
            data = json_decode(self.request.body)

            response = self.service.post(self.request.uri, data)

            log.info("Widget POST request successfully. "
                     "Request URL: {0}. "
                     "Request body: {1}. "
                     .format(self.request.uri, data))

            return self.success(response, 200)

        except Exception as e:
            log.error("Widget POST request error."
                      "Request URL: {0}. "
                      "Request body: {1}. "
                      "Exception: {2}. "
                      .format(self.request.uri, self.request.body, e))

            return self.error({
                "message": "Widget POST request error."
                           "Request URL: {0}. "
                           "Request body: {1}. ".format(self.request.uri, self.request.body)}, 500)

    @validate.put
    def put(self, id):
        """
        Method PUT to API restful widget

        :type id: int
        :param id: It's the widget id will be updated.

        :returns: json -- to sync requests (200) | empty string ("").

        :raises: Exception (500)
        """
        try:

            # Getting body + url
            data = json_decode(self.request.body)
            data.update({"id": id})

            response = self.service.put(self.request.uri, data)

            log.info("Widget PUT request successfully. "
                     "Request URL: {0}. "
                     "Request body: {1}. "
                     .format(self.request.uri, data))

            return self.success(response, 200)

        except Exception as e:
            log.error("Widget PUT request error. "
                      "Request URL: {0}. "
                      "Request body: {1}. "
                      "Exception: {2}. "
                      .format(self.request.uri, self.request.body, e))

            return self.error({
                "message": "User PUT request error."
                "Request URL: {0}. "
                "Request body: {1}. " . format(self.request.uri, self.request.body)}, 500)

    @validate.delete
    def delete(self, id):
        """
        Method DELETE to API restful widget

        :type id: int
        :param id: It's the widget id will be deleted.

        :returns: json -- to sync requests (200) | empty string ("").

        :raises: Exception (500)
        """
        try:
            data = {"id": id}

            response = self.service.delete(self.request.uri, data)

            log.info("Widget DELETE request successfully. "
                     "Request URL: {0}. "
                     "Request body: {1}. "
                     .format(self.request.uri, data))

            return self.success(response, 200)

        except Exception as e:
            log.error("Widget DELETE request error. "
                      "Request URL: {0}. "
                      "Request body: {1}. "
                      "Exception: {2}. "
                      .format(self.request.uri, self.request.body, e))

            return self.error({
                "message": "Bundle DELETE request error."
                "Request URL: {0}. "
                "Request body: {1}. " . format(self.request.uri, self.request.body)}, 500)
