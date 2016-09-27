# -*- encoding: utf-8 -*-

"""
Random features goes here.
"""
import codecs
import datetime
import application.settings as settings
from uuid import UUID
from tornado.escape import json_decode, json_encode

DOCUMENT_REQUEST = "document"
EMAIL_REQUEST = "email"
MSISDN_REQUEST = "msisdn"
UUID_REQUEST = "uuid"
POST_REQUEST = "post"
PUT_REQUEST = "put"
GET_REQUEST = "get"
DELETE_REQUEST = "delete"


def decode(bytes):
    """
    Decodes bytes to string.
    :param bytes:
    :return:
    """
    return bytes.decode(settings.APPLICATION_ENCODING)


def encode(bytes):
    """
    Encode bytes to string.
    :param bytes:
    :return:
    """
    return bytes.encode(settings.APPLICATION_ENCODING)


def row2dict(row):
    """
    Turns a row into a dict.
    :param row:
    :return: dict
    """
    d = {}
    for column in row.__table__.columns:
        if type(getattr(row, column.name)) == UUID:
            d[column.name] = str(getattr(row, column.name))
            continue
        if isinstance(getattr(row, column.name), datetime.datetime):
            d[column.name] = str(getattr(row, column.name))
            continue
        try:
            d[column.name] = int(getattr(row, column.name))
        except:
            d[column.name] = getattr(row, column.name)
    return d


def list2dict(list):
    """
    Turns a list into a dict.
    :param list:
    :return: dict
    """
    return {"{0}".format(item.key): row2dict(item) for item in list}


def list2dict(list, key):
    """
    Turns a list into a dict.
    :param list:
    :return: dict
    """
    return {"{0}".format(eval("item.{0}".format(key))): row2dict(item) for item in list}


def get_config_map(configs):
    """
    Turns a list into a dict.
    :param configs:
    :return: dict
    """
    return {item.key: row2dict(item) for item in configs}


def get_headers(headers, filter=None):
    """
    Turns tornado headers into a dict.
    :param headers:
    :param filter:
    :return: dict
    """
    filter = headers.keys() if filter is None else filter
    filter = [key.upper() for key in filter]  # Uppercase to avoid case sensitive issues.

    return {key: value for (key, value) in headers.get_all() if key.upper() in filter}


def get_optional_key(json, key, default_value=None):
    """
    Get an optional value from a dict.
    :param json:
    :param key:
    :param default_value:
    :return:
    """
    try:
        return json[key]
    except KeyError:
        return default_value


def zlib_to_json(zlib):
    """
    Turns a zlib string into a json.
    :param zlib: str
    :return: dict
    """
    return json_decode(decode_zlib(zlib))


def json_to_zlib(json):
    """
    Turns a json into a zlib string.
    :param json: dict
    :return: str
    """
    return codecs.encode(bytes(json_encode(json), settings.APPLICATION_ENCODING), "zlib")


def decode_zlib(zlib):
    """
    Decodes a zlib string.
    :param zlib: str
    :return: str
    """
    return decode(codecs.decode(zlib, "zlib"))


def get_recursively(key, search_dict):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a given key.
    :param search_dict:
    :param key:
    :return:
    """
    fields_found = []
    for key_, value in search_dict.items():

        if key_ == key:
            fields_found.append(value)

        elif isinstance(value, dict):
            results = get_recursively(key, value)
            for result in results:
                fields_found.append(result)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = get_recursively(key, item)
                    for another_result in more_results:
                        fields_found.append(another_result)

    return fields_found


def str2bool(string):
    """
    Converts string to bool
    :param string:
    :return: bool
    """
    return string.lower() in ("yes", "true", "t", "1")
