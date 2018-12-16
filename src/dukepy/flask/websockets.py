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
    # Catch all events
    # For JS | https://stackoverflow.com/questions/10405070/socket-io-client-respond-to-all-events-with-one-handler
    def trigger_event(self, event, *args):
        """Dispatch an event to the proper handler method.

        In the most common usage, this method is not overloaded by subclasses,
        as it performs the routing of events to methods. However, this
        method can be overriden if special dispatching rules are needed, or if
        having a single method that catches all events is desired.
        """
        handler_name = 'on_' + event
        print(handler_name)
        if not hasattr(self, handler_name):
            # there is no handler for this event, so we ignore it
            return
        handler = getattr(self, handler_name)
        return self.socketio._handle_event(handler, event, self.namespace,
                                           *args)

    def on_connect(self):
        emit('my response', {'data': 'welcome!'})

    def on_disconnect(self):
        print('Client disconnected')

    def on_fire(self, cmd):
        fire_task_wrapper(cmd, emit)

    def on_echo(self, message):
        emit('my response', {'data': message['data']})


socketio.on_namespace(SocketNamespace('/websocket'))
