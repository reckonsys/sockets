import eventlet
from redis_app import sio
from socketio import WSGIApp


@sio.event
def connect(sid, environ):
    user_socket_id = environ['HTTP_USER_SOCKET_ID']
    sio.enter_room(sid, user_socket_id)
    sio.emit('notify_user', {'to': 'user_socket_id'}, to='sample_socket_id')


@sio.event
def disconnect(sid):
    # user_socket_id = environ['HTTP_USER_SOCKET_ID']
    # sio.leave_room(sid, user_socket_id)
    pass


if __name__ == '__main__':
    eventlet.monkey_patch()
    app = WSGIApp(sio)
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
