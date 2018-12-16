from enum import Enum
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dukepy.config import Config

Base = declarative_base()


class DBType(Enum):
    sqlite = 1
    mysql = 2
    postgres = 3


class DBSession():

    def __init__(self):
        pass

    def uri(self):
        db_uri = None

        if db_type == DBType.sqlite:
            db_uri = "sqlite:///" + Config()["database"]["sqlite"]["path"]

        if db_type == DBType.mysql:
            config = Config()["database"]["mysql"]
            db_uri = "mysql+pymysql://{0}:{1}@{2}:3306/{3}".format(config["user"], config["password"], config["host"],
                                                                   config["db"])

        if db_type == DBType.postgres:
            config = Config()["database"]["postgres"]
            db_uri = "postgresql://{0}:{1}@{2}:{3}/{4}".format(config["user"], config["password"], config["host"],
                                                               config["port"], config["db"])

        return db_uri

    def engine(self):
        _engine = create_engine(self.uri())
        return _engine

    def db_type(self):
        ret = DBType.sqlite  # Default
        if "sqlite" == Config()["database"]["active"]:
            ret = DBType.sqlite
        if "mysql" == Config()["database"]["active"]:
            ret = DBType.mysql
        if "postgres" == Config()["database"]["active"]:
            ret = DBType.postgres
        return ret


_helper = DBSession()
db_type = _helper.db_type()


def _session_factory():
    Base.metadata.create_all(_helper.engine())

    session = sessionmaker(bind=_helper.engine())()
    session._model_changes = {}
    return session


db_session = _session_factory
