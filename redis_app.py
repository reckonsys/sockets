import json
from redis import Redis

MESSAGE = 'msg'
USER_SOCKET_ID = 'user_socket_id'
SERVER_CHANNEL = 'edvay-server-channel'
redis = Redis(host='localhost', port=6379, db=0)


def _send(user_socket_id, msg):
    redis.publish(SERVER_CHANNEL, json.dumps({
        USER_SOCKET_ID: user_socket_id,
        MESSAGE: msg,
    }))

