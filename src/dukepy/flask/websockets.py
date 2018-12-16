from flask_socketio import emit, Namespace

from dukepy.fire.fire_cli import fire_task_wrapper
from dukepy.flask import socketio


@socketio.on('my event', namespace='/test')
def test_message(message):
    print(message)
    emit('my response', {'data': message['data']})


@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


class SocketNamespace(Namespace):
    def on_connect(self):
        emit('my response', {'data': 'welcome!'})

    def on_disconnect(self):
        print('Client disconnected')

    def on_fire(self, cmd):
        fire_task_wrapper(cmd, emit)

    def on_echo(self, message):
        emit('my response', {'data': message['data']})


socketio.on_namespace(SocketNamespace('/websocket'))
