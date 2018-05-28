import json
import time
import uuid
import base64
import _thread

import asyncio
import websockets

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from flask import Flask, make_response, request
from flask_socketio import SocketIO, disconnect
from gevent import monkey

import aes

aes_key = "SUPER_SEXY_MOAI_"

app = Flask(__name__)
app.config['SECRET_KEY'] = uuid.uuid4()

socketio = SocketIO(app)
monkey.patch_all()

def to_encrypt(s):
    return aes.AESCipher(aes_key).encrypt(s)

def to_decrypt(s):
    return aes.AESCipher(aes_key).decrypt(s)

@app.route('/')
def handle_client_registion():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        message = ws.read_message()
    try:
        json_object = json.loads(message)
    except ValueError as e:
        return False

    if 'authkey' in json_object:
        key = str(json_object['authkey'])
        encrypted_key = to_encrypt(key)
        # create new socket event using namespace that create by AES(key)
        print("[*] Create a new socket event uri '{}' by {}"\
                    .format(encrypted_key, key))
        app.add_url_rule('/%s' % encrypted_key, view_func=each_client_index)
        ws.send(encrypted_key)
    ws.close()
    return make_response()

def each_client_index():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        print("[*] Connected client socket ")
        while True:
            message = 'hello'
            ws.send(message)
            time.sleep(1)
        print("[ ] Disconnected client socket ")
        ws.close()
    return make_response()

if __name__ == '__main__':
    http_server = WSGIServer(('', 5001), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
