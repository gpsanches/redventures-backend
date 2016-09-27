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
        r"/widgets/([0-9]+)(?:/)?",
    ]

    # Service
    service = services.WidgetService()

    @validate.get
    def get(self):
        """
        Receives GET requests.
        :return:
        """
        try:
            # Getting body
            data = json_decode(self.request.body)

            response = self.service.get(self.request.uri, data)

            log.info("Widgets GET request successfully. ")

            return self.success(response, 200)

        except Exception as e:
            # Log
            log.error("Widgets GET request Error."
                      "Exception: {0}. "
                      .format(e))

            # Return error
            return self.error({"success": 0, "message": "GET request Error!"}, 500)

    # @validate.post
    # def post(self):
    #     """
    #     Receives POST requests.
    #     :return:
    #     """
    #
    # @validate.put
    # def put(self, id):
    #     """
    #     Receives PUT requests.
    #     :return:
    #     """