from dukepy.config import Config
from dukepy.flask import app

config = Config()


# from scripts.create_db_schema import initDB
# initDB()

if __name__ == '__main__':
    debug = config["debug"]
    host = config["server"]["host"]
    port = config["server"]["port"]
    app.run(port=port, debug=debug, host=host, threaded=True)
