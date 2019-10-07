import json
import eventlet
import socketio
from redis_app import redis, SERVER_CHANNEL, USER_SOCKET_ID  # , MESSAGE


ROOM_PREFIX = "ROOM_%s"
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
pubsub = redis.pubsub()


def _sid_set(user_socket_id, sid):
    return redis.set(ROOM_PREFIX % user_socket_id, sid)


def _get_sid(user_socket_id):
    return redis.get(ROOM_PREFIX % user_socket_id).decode()


@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.event
def my_message(sid, data):
    print('message ', data)


@sio.event
def join_room(sid, user_socket_id):
    _sid_set(user_socket_id, sid)
    sio.enter_room(sid, user_socket_id)
    sid = _get_sid(user_socket_id)
    print("join_room", sid)
    sio.emit('notify_user', {'data': 'foobar'}, room=sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


def server_channel_handler(message):
    message = json.loads(message['data'].decode())
    user_socket_id = message[USER_SOCKET_ID]
    # msg = message[MESSAGE]
    sid = _get_sid(user_socket_id)
    print("server_channel_handler", sid)
    sio.emit('notify_user', {'data': 'foobar'}, room=sid)


if __name__ == '__main__':
    pubsub.subscribe(**{SERVER_CHANNEL: server_channel_handler})
    pubsub.run_in_thread(sleep_time=0.1)
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
