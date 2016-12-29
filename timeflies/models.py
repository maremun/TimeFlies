#   encoding: utf8
#   models.py

import enum

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Enum, ForeignKey, \
        create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import scoped_session, sessionmaker, relationship


def connect_database(uri):
    sess = scoped_session(sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=create_engine(uri, pool_recycle=3600)))

    return sess


class UnitEnum(enum.Enum):

    h = 'hours'
    d = 'days'
    w = 'weeks'
    m = 'months'
    y = 'years'


@as_declarative()
class Base(object):

    pass


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=True)
    first_name = Column(String(64), nullable=True)
    last_name = Column(String(64), nullable=True)
    last_seen_at = Column(DateTime, default=datetime.now, nullable=False)
    # state is a s|timelapse_id user is working with
    # 'start|-1' for starting state
    # 'track|-1' for tracking state
    # 'add|123' for adding timelapse with id=123
    # 'units|123' for editing timelapse (id=123) measure units
    # 'edit|123' for editing timelapse menu for timelapse with id=123
    state = Column(String(64), default='start|-1', nullable=False)

    timelapses = relationship('Timelapse', back_populates='user',
                              cascade='all, delete, delete-orphan')

    def __repr__(self):
        template = '<User[{0:d}] {1:s}>'
        return template.format(self.id, self.username)


class Timelapse(Base):
    # TODO Impose constrains on the entries
    # (uniqueness of Timelapse name for user, etc).

    __tablename__ = 'timelapses'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'))
    title = Column(String(64), nullable=False, unique=True)
    units = Column(Enum(UnitEnum), default=UnitEnum.w, nullable=False)
    duration = Column(Integer, default=3, nullable=False)
    start_time = Column(DateTime, default=datetime.now, nullable=False)
    progress = Column(Integer, default=0, nullable=False)

    user = relationship('User', back_populates='timelapses')

    def __repr__(self):
        template = "<Timelapse[id={:d}] name='{:s}' started {:s} " \
                   "duration: {:d} {:s}.>"
        return template.format(self.id, self.title, str(self.start_time),
                               self.duration, self.units.value)
