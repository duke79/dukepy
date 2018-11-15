from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from dukepy.config import Config

config = Config()

app = Flask(__name__)
CORS(app, origins=config["allowed_domains"])  # Allow cross-domain
# app.wsgi_app = ProxyFix(app.wsgi_app)
socketio = SocketIO(app)

import dukepy.flask.views
import dukepy.flask.websockets
