import sys
import threading

from io import StringIO
import asyncio
from multiprocessing import Process

import fire
from flask_socketio import emit, Namespace

from cli.fire.fire_cli import Root, fire_task_wrapper
from dukepy.flask import socketio
from dukepy.processify import processify


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

    def on_message(self, message):
        print(message)
        emit('my response', {'data': 'custom message'})
        fire_task_wrapper(message, emit)

    def on_echo(self, message):
        print(message)
        emit('my response', {'data': message['data']})


socketio.on_namespace(SocketNamespace('/custom'))


# socketio.emit("my response", "asynco") #has no effect


## USELESS
# async def async_loop():
#     for i in range(100):
#         await asyncio.sleep(3)
#         socketio.emit("my response", "asynco")
#         print("asynco")
#
#
# loop = asyncio.get_event_loop()
# # loop.run_until_complete(async_loop())
# # loop.close()