from sqlalchemy import Column, String

# from app import db
from data.common import Base
# from flask_sqlalchemy import Model
from data.common.mixin import Mixin


class MyTable(Mixin, Base):
	name = Column(String(200), nullable=True)
	trigram = Column(String(200), nullable=True)
	machine = Column(String(200), nullable=True)
	# hobby = Column(String(200), nullable=True)

	def __init__(self, name, trigram):
		self.name = name
		self.trigram = name
