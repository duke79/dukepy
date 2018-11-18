from sqlalchemy import Column, String

from data.common import Base
from data.common.mixin import Mixin


class Person(Mixin, Base):
	name = Column(String(200), nullable=True)

	def __init__(self, name):
		self.name = name
