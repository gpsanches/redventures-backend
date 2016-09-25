# -*- encoding: utf-8 -*-

from functools import wraps
from tornado.escape import json_decode
import logging
import application.settings as settings
from application.src.validators import Validators
from application.src.exceptions import InvalidData
from modules.users.v1.settings import MODULE_NAME


# Logging handler
log = logging.getLogger(__name__)
LOG_HASH_SAMPLE = settings.LOG_HASHES[MODULE_NAME]["sample"]


def get(func):
    """
    Validates request: mandatory parameters and configs.
    """
    @wraps(func)
    def structure(self, id=None):

        schema = {
            "type": "object", "properties": {
                "id": {"required": False, "type": "integer"},
            }
        }

        try:
            data = {}

            # add fields from url in data to validation
            data.update({
                "id": id,
            })

        except Exception:
            log.error("Could not do it. "
                      "Error: Invalid JSON. ")
            return self.error({"message": "Invalid JSON"})

        try:
            Validators.validate_schema(data, schema)
        except Exception as error:
            log.error("Could not do it. "
                      "Error: Invalid Schema: {0}. ")
            return self.error({"message": "{0}" . format(error)})

        return func(self, id)
    return structure
