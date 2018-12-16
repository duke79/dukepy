from sqlalchemy import Column, String
from dukepy.data.common import Base
from dukepy.data.common.mixin import Mixin


class FireCommand(Mixin, Base):
    cmd = Column(String(200), nullable=True)
    source = Column(String(200), nullable=True)

    def __init__(self, cmd="", source=""):
        self.cmd = cmd
        self.source = source
