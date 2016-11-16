from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base


@declarative_base
class Base(object):

	pass


class User(Base):

	__tablename__ = 'users'

	id = Column(Integer, primary_key=True) 
	username = Column(String(64), nullable=False)
	first_name = Column(String(64), nullable=True)
	last_name = Column(String(64), nullable=True)
	last_seen_at = Column(DateTime, default=datetime.now, nullable=False)

	def __repr__(self):
		template = '<User[{0:s}] {1:s}>'
		return template.format(self.id, self.username)
