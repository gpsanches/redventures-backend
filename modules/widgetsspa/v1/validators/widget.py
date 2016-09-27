# -*- encoding: utf-8 -*-

from functools import wraps
from tornado.escape import json_decode
import logging
import application.settings as settings
from application.src.validators import Validators
from application.src.exceptions import InvalidData
from modules.widgetsspa.v1.settings import MODULE_NAME


# Logging handler
log = logging.getLogger(__name__)


def get(func):
    """
    Validates request: mandatory parameters.
    """
    @wraps(func)
    def structure(self, filter=None):

        schema = {
            "type": "object", "properties": {
                "filter": {"required": False, "format": "filter"},
            }
        }

        try:
            data = {}

            # add fields from url in data to validation
            data.update({"filter": filter})

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

        return func(self, filter)
    return structure


def post(func):
    """
    Validates request: mandatory parameters.
    """
    @wraps(func)
    def structure(self):

        schema = {
            "type": "object", "properties": {
                "name": {"required": True, "type": "string"},
                "color": {"required": True, "type": "string"},
                "price": {"required": True, "type": "number"},
                "inventory": {"required": True, "type": "integer"},
                "melts": {"required": True, "type": "boolean"},
            }
        }

        try:
            data = json_decode(self.request.body)

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

        return func(self)
    return structure


def put(func):
    """
    Validates request: mandatory parameters.
    """
    @wraps(func)
    def structure(self, id):

        schema = {
            "type": "object", "properties": {
                "id": {"required": True, "type": "integer"},
                "name": {"required": False, "type": "string"},
                "color": {"required": False, "type": "string"},
                "price": {"required": False, "type": "number"},
                "inventory": {"required": False, "type": "integer"},
                "melts": {"required": False, "type": "boolean"},
            }
        }

        try:
            data = json_decode(self.request.body)
            data.update({"id": int(id)})

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


def delete(func):
    """
    Validates request: mandatory parameters.
    """
    @wraps(func)
    def structure(self, id):

        schema = {
            "type": "object", "properties": {
                "id": {"required": True, "type": "integer"},
            }
        }

        try:
            data = ({"id": int(id)})

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
