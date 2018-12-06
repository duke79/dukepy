from flask_socketio import emit, Namespace

from fire_cli import fire_task_wrapper
from flask_socketio import SocketIO
from app import app

socketio = SocketIO(app)


class Websocket(Namespace):
	def on_connect(self):
		# print('Client connected')
		emit('fireout', {'data': 'welcome!'})

	def on_disconnect(self):
		print('Client disconnected')  # DO NO REMOVE THIS LINE, TO HANDLE MULTIPLE CONNECTIONS
		pass

	def on_message(self, message):
		# print(message)
		emit('message', {'data': 'custom message'})

	def on_fire(self, message):
		# print(message)
		# emit("fireout,""sdfsd")
		fire_task_wrapper(message, emit)

	def on_echo(self, message):
		# print(message)
		emit('echo', {'data': message['data']})


socketio.on_namespace(Websocket('/websocket'))
