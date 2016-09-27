# -*- encoding: utf-8 -*-

import logging
from tornado.escape import json_decode
import application.settings as settings
from application.src.rewrites import APIHandler
from modules.widgetsspa.v1.services import user as services
from modules.widgetsspa.v1.validators import user as validate
from modules.widgetsspa.v1.settings import MODULE_NAME, MODULE_VERSION


# Logging
log = logging.getLogger(__name__)


class UserHandler(APIHandler):

    __urls__ = [
        # get
        r"/users(?:/)?",

        # get or post with id
        r"/users/([0-9]+)(?:/)?",
    ]

    # Service
    service = services.UserService()

    @validate.get
    def get(self, filter=None):
        """
        Receives POST requests.
        :return:
        """
        try:
            # Getting body
            data = {"filter": filter}

            response = self.service.get(self.request.uri, data)

            log.info("Users GET request successfully. ")

            return self.success(response, 200)

        except Exception as e:
            # Log
            log.error("Users GET request Error."
                      "Exception: {0}. "
                      .format(e))

            # Return error
            return self.error({"success": 0, "message": "GET request Error!"}, 500)
