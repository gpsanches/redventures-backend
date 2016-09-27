# -*- encoding: utf-8 -*-

import validators
import validictory
import datetime
from application.src import exceptions


class Validators(object):
    """
    Class which holds validation rules.
    """

    @staticmethod
    def validate_datetime(validator, fieldname, value, format_option):
        """
        Validates datetime.
        :param validator:
        :param fieldname:
        :param value:
        :param format_option:
        :return:
        """
        try:
            datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

        except Exception:
            raise validictory.FieldValidationError("invalid datetime format. It must be yyyy-mm-dd hh:mm:ss",
                                                   fieldname, value)

    @staticmethod
    def validate_uuid(validator, fieldname, value, format_option):
        """
        Validates UUID.
        :param validator:
        :param fieldname:
        :param value:
        :param format_option:
        :return:
        """
        if not validators.uuid(value):
            raise validictory.FieldValidationError("invalid UUID", fieldname, value)

    @staticmethod
    def validate_filter(validator, fieldname, value, format_option):
        """
        Validates filters.
        :param validator:
        :param fieldname:
        :param value:
        :param format_option:
        :return:
        """
        if not isinstance(value, int):
            if not isinstance(value, str):
                raise validictory.FieldValidationError("invalid filter", fieldname, value)

    @staticmethod
    def validate_email(validator, fieldname, value, format_option):
        """
        Validates EMAIL.
        :param validator:
        :param fieldname:
        :param value:
        :param format_option:
        :return:
        """
        if not validators.email(value):
            raise validictory.FieldValidationError("invalid Email", fieldname, value)

    @staticmethod
    def validate_url(validator, fieldname, value, format_option):
        """
        Validates URL.
        :param validator:
        :param fieldname:
        :param value:
        :param format_option:
        :return:
        """
        if not validators.url(value):
            raise validictory.FieldValidationError("invalid Url", fieldname, value)

    @classmethod
    def validate_schema(cls, data, schema):
        """
        Validates data through a schema.
        :param data:
        :param schema:
        :return:
        """
        try:
            custom_validators = {
                "uuid": cls.validate_uuid,
                "datetime": cls.validate_datetime,
                "email": cls.validate_email,
                "url": cls.validate_url,
                "filter": cls.validate_filter,
            }

            validictory.validate(
                    data,
                    schema,
                    format_validators=custom_validators
            )

        except Exception as e:
            raise exceptions.InvalidData(e)
