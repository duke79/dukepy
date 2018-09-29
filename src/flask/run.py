from app import app
from flask_cors import CORS, cross_origin
from app.data.config import Config

config = Config()

'''Run app'''
CORS(app, origins=config["allowed_domains"])  # Allow cross-domain
debug = config["debug"]
host = config["server"]["host"]
port = config["server"]["port"]
app.run(port=port, debug=debug, host=host, threaded=True)
