# -*- encoding: utf-8 -*-

from application import settings
from application.src import databases
from modules.users.v1.settings import MODULE_NAME


def get_db_connections():
    """
    Returns database connections for current module.
    :return: dict
    """
    mysql_configs = settings.DATABASES['application']["mysql-configs"]
    if "mysql-configs" in settings.DATABASES[MODULE_NAME]:
        mysql_configs = settings.DATABASES[MODULE_NAME]["mysql-configs"]

    return {
        'mysql': databases.DB().get_instance(
            name=MODULE_NAME,
            data=settings.DATABASES[MODULE_NAME]["mysql"],
            configs=mysql_configs
        ),
    }
