# -*- encoding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, Float, String, Text, DateTime, MetaData, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator, CHAR
from tornado.escape import json_decode, json_encode
import uuid
import datetime

Base = declarative_base()


class Json(TypeDecorator):
    # TODO: SqlAlchemy1.1 has a native type but it's in development version yet.
    """
    Platform-independent Json type.
    Uses TEXT type as Json
    """
    impl = Text

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(Text)

    def process_bind_param(self, value, dialect):
        if type(value) == dict:
            return json_encode(value)
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return json_decode(value)


class DefaultBase(Base):
    __abstract__ = True
    metadata = MetaData()


class Config(DefaultBase):
    __tablename__ = 'configs'

    id = Column(TINYINT(unsigned=True), primary_key=True)
    key = Column(String(255), unique=True, nullable=False)
    value = Column(String(255), nullable=False)


class Users(DefaultBase):
    """
    Table Users definition
    """
    __tablename__ = 'users'

    id = Column(TINYINT(unsigned=True), primary_key=True)
    name = Column(String(255), nullable=False)
    gravatar = Column(String(255), nullable=True)


class Widgets(DefaultBase):
    """
    Table Users definition
    """
    __tablename__ = 'widgets'

    id = Column(TINYINT(unsigned=True), primary_key=True)
    name = Column(String(255), nullable=False)
    color = Column(String(255), nullable=False)
    price = Column(Float(precision=2), nullable=False)
    inventory = Column(TINYINT(unsigned=True), nullable=False)
    melts = Column(Boolean, nullable=False)
