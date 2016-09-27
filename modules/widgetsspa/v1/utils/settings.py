# -*- encoding: utf-8 -*-

from application.src import utils
from application import settings
from modules.widgetsspa.v1.models import Config


def get_settings(db_connections):
    """
    Returns settings for current module.
    :param: db_connections
    :return: dict
    """
    return {
        "configs": utils.get_config_map(db_connections['mysql'].query(Config).all()),
        "debug": settings.DEBUG
    }
