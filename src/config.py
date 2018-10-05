import json
import os

from app.utils.singleton import Singleton


class ConfigError(Exception):
    pass


class Config(dict, metaclass=Singleton):
    def __str__(self):
        return json.dumps(self.config, indent=4)

    def __init__(self):
        dict.__init__(self, dict())  # Because dict is extended

        # Open src/flask/config/config.json
        # file_dir = os.path.abspath(__file__)
        # flask_dir = os.path.dirname(os.path.dirname(os.path.dirname(file_dir)))
        # self.config_dir = os.path.join(flask_dir, "config")
        self.config_dir = os.path.join(os.path.expanduser("~"), ".samanvaya")
        self.config_file = os.path.join(self.config_dir, "config.json")

        # create config.json and initialize empty self.config
        if not os.path.exists(self.config_file):
            if not os.path.exists(self.config_dir):
                os.mkdir(self.config_dir)  # Create directory
            open(self.config_file, "a").close()  # Create empty file
            self.config = dict()
            self.initDefaults()  # Initialize with default values
            self.commit()

        # initialize self.config from config.json
        with open(self.config_file, "r+") as f:
            conf = f.read()
            if conf != "":
                try:
                    self.config = json.loads(conf)
                except json.decoder.JSONDecodeError as e:
                    raise ConfigError("Config file invalid format")
            else:
                self.config = dict()

    def __enter__(self):
        """ to enable 'with **' capability, counterpart function is __exit__ """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ commit at the end of 'with **' block """
        self.commit()

    def __getitem__(self, key):
        # return super().__getitem__(key)
        try:
            return self.config[key]
        except KeyError as e:
            self.__setitem__(key, dict())  # initialize the non-existent keys
            return self.config[key]

    def __setitem__(self, key, value):
        # super().__setitem__(key, value)
        self.config[key] = value

    def commit(self):
        """
        Commit the configuration changes to file
        Use "with Config() as config" if auto commit is needed at the end,
        otherwise use this method.
        """
        # make a copy of the original config
        from shutil import copyfile
        copyfile(self.config_file, self.config_file + ".old")

        # overwrite the file with new config
        with open(self.config_file, "w+") as f:
            json.dump(self.config, f, indent=4)

    def initDefaults(self):
        self.config["server"] = {
            "host": "0.0.0.0",
            "port": "80"
        }
        self.config["database"] = {
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
        }
        self.config["debug"] = False
        self.config["stacktrace"] = False
        self.config["allowed_domains"] = ["http://1", "http://2"]


if __name__ == "__main__":
    with Config() as config:
        pass

        # config.commit() #Not required, since we are using with*
