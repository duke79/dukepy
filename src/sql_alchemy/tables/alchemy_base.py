import datetime
import traceback

from sqlalchemy import create_engine, Column, DateTime, func
from sqlalchemy.exc import DatabaseError
from flask_sqlalchemy import Model
from sqlalchemy.orm import sessionmaker

from app import Config
from app.utils.traces import print_exception_traces


## Init session
class DBSession():
    def uri_sqlite(self):
        db_uri = "sqlite:///sqlalchemy_example.db"
        return db_uri

    def uri_mysql(self):
        config = Config()["database"]["mysql"]
        db_uri = "mysql+pymysql://{0}:{1}@{2}:3306/{3}".format(config["user"], config["password"], config["host"],
                                                               config["db"])
        return db_uri

    def uri_postgres(self):
        config = Config()["database"]["postgres"]
        db_uri = "postgresql://{0}:{1}@{2}:{3}/{4}".format(config["user"], config["password"], config["host"],
                                                           config["port"], config["db"])
        return db_uri

    def create_session(self, db_uri):
        engine = create_engine(db_uri)
        Session = sessionmaker(bind=engine)
        session = Session()
        session._model_changes = {}
        return session


db_session_helper = DBSession()
# db_uri = db_session_helper.uri_mysql()
db_uri = db_session_helper.uri_postgres()
# db_uri = db_session_helper.uri_sqlite()
db_session = db_session_helper.create_session(db_uri)


## Declare base
class AlchemyBase(Model):
    """
    ref: https://chase-seibert.github.io/blog/2016/03/31/flask-sqlalchemy-sessionless.html
    """

    # https://stackoverflow.com/a/12155686/973425
    created_at = Column(DateTime, nullable=False,
                        server_default=func.now())
    updated_at = Column(DateTime, nullable=False,
                        server_default=func.now(),
                        server_onupdate=func.now())

    def save(self):
        local_object = db_session.merge(self)
        db_session.add(local_object)
        # try:
        self._flush()
        db_session.commit()
        # except DatabaseError as e:
        #     code = e.orig.args[0]
        #     if code == 1062:
        #         raise
        #     return None
        return local_object

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()

    def delete(self):
        local_object = db_session.merge(self)  # https://stackoverflow.com/a/47663833/973425
        db_session.delete(local_object)
        self._flush()
        db_session.commit()

    def _flush(self):
        try:
            db_session.flush()
            # db_session.refresh(self)
        except DatabaseError as e:
            db_session.rollback()
            print_exception_traces(e)
            raise

    @staticmethod
    def session():
        return db_session
