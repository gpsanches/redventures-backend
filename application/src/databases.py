# -*- encoding: utf-8 -*-

import logging
import importlib
from application.src import exceptions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from application import settings

# Logging handler
log = logging.getLogger(__name__)


class DB(object):
    """
    Database connection class.
    For further explanations read this: http://docs.sqlalchemy.org/en/rel_1_1/orm/session_transaction.html
    """
    # Static property
    instance = {}
    engine = {}

    @classmethod
    def get_instance(cls, name, data, configs):
        """
        Returns DB instance (singleton).
        :return: DBSession
        """
        if name in cls.instance:
            return cls.instance[name]

        engine = cls.get_engine(name, data, configs)
        models = importlib.import_module('modules.{0}.v1.models'.format(name))
        models.DefaultBase.metadata.create_all(engine)

        session = sessionmaker(autocommit=True, bind=engine)
        cls.instance[name] = scoped_session(session)()

        return cls.instance[name]

    @classmethod
    def get_engine(cls, name, data, configs):
        if name in cls.engine:
            return cls.engine[name]

        cls.engine[name] = create_engine(
                cls.get_connection_string(data),
                logging_name=name,
                pool_recycle=configs['pool_recycle'],
                pool_size=configs['pool_size'],
                max_overflow=configs['max_overflow'],
                pool_timeout=configs['timeout']
            )

        return cls.engine[name]

    @staticmethod
    def get_connection_string(connection):
        return "{0}://{1}:{2}@{3}:{4}/{5}?charset={6}"\
            .format(connection['ENGINE'],
                    connection['USER'], connection['PASSWORD'],
                    connection['HOST'], connection['PORT'],
                    connection['NAME'], connection['CHARSET'])