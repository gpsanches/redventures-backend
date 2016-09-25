# -*- encoding: utf-8 -*-

import logging
from tornado.escape import json_decode
import application.settings as settings
from application.src.rewrites import APIHandler
from modules.users.v1.services import user as services
from modules.users.v1.validators import user as validate
from modules.users.v1.settings import MODULE_NAME, MODULE_VERSION


# Logging
log = logging.getLogger(__name__)


class UserHandler(APIHandler):

    __urls__ = [
        # get
        r"/{0}(?:/)?".format(MODULE_NAME),

    ]

    # Service
    service = services.UserService

    @validate.get
    def get(self):
        """
        Receives POST requests.
        :return:
        """
        try:
            # Getting body
            body = json_decode(self.request.body)
            phrase = body['phrase']

            # Doing sample (async)
            self.service.write_file.delay(phrase)

            # Log
            log.info("We have queued it. "
                     "Request body: {0}. "
                     .format(body))

            # Return success
            return self.success({"success": 1, "message": "Done!"})

        except Exception as e:
            # Log
            log.error("Could not queue it. "
                      "Error: An unexpected error occurred. "
                      "Exception: {0}. "
                      .format(e))

            # Return error
            return self.error({"success": 0, "message": "Could not do it!"}, 500)
