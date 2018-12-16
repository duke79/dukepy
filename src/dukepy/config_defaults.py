import getpass
import os
import socket
from os.path import expanduser


def config_defaults():
    defaults = dict()

    home_config = os.path.join(expanduser("~"), "dukepy")
    sqlite_path = os.path.join(home_config, os.path.normpath("sqlite.db"))
    dev_home = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    defaults["home"] = home_config

    defaults["server"] = {
        "host": "0.0.0.0",
        "port": "5555"
    }

    defaults["database"] = {
        "active": "sqlite",
        "mysql": {
            "db": "dummy_db",
            "user": "dummy_user",
            "host": "localhost",
            "password": "dummy_password"
        },
        "postgres": {
            "db": "dummy_db",
            "user": "dummy_user",
            "host": "localhost",
            "password": "dummy_password",
            "port": "5432"
        },
        "sqlite": {
            "path": sqlite_path
        },
        "firebase": {
            "service_account_key": "path_to_serviceAccountKey.json",
            "databaseURL": "https://xyz_project_123.firebaseio.com"
        }
    }

    return defaults
