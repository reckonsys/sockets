from socketio import RedisManager, Server

mgr = RedisManager('redis://localhost:6379/0')  # , write_only=True)
sio = Server(client_manager=mgr, cors_allowed_origins='*')


def _send(user_socket_id, msg):
    sio.emit('notify_user', {'data': msg}, room=user_socket_id)
