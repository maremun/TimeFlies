import enum

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Enum, ForeignKey, \
        create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import scoped_session, sessionmaker


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

	def __repr__(self):
		template = '<User[{0:s}] {1:s}>'
		return template.format(self.id, self.username)


class Timelapse(Base):

    __tablename__ = 'timelapse' 

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'))
    timelapse_name = Column(String(64), nullable=False)
    units = Column(Enum(UnitEnum), nullable=False)
    duration = Column(Integer, nullable=False)
    start_time = Column(DateTime, default=datetime.now, nullable=False)
    progress = Column(Integer, nullable=False)

    def __repr__(self):
        template = '<Timelapse[id={:s}] name={:s} started {:s} progress {:s} {:s}.>'
        return template.format(self.id, self.timelapse_name, str(self.start_time), self.duration, self.units)



