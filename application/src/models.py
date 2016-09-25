# -*- encoding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.mutable import MutableDict
import datetime

Base = declarative_base()


class DefaultBase(Base):
    __abstract__ = True
    metadata = MetaData()


class Config(DefaultBase):
    __tablename__ = 'configs'
    id = Column(Integer, primary_key=True)
    config = Column(MutableDict.as_mutable(HSTORE), nullable=True)
    key = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)

