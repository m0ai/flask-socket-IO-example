#-*- coding: utf-8 -*-
import os
import sys
import json
import time
import urllib.parse

import websocket

class ClientAuthSocket:
    def __init__(self, uri):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(uri,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)

    def ws_comm(self):
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def on_message(self, ws, message):
        try:
            print(message)
        except Exception as e:
            print(e)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        ws.send('moai')
        pass


class ClientRegisterSocket:
    def __init__(self, uri):
        websocket.enableTrace(True)
        self.crypted_auth = ""
        self.ws = websocket.WebSocketApp(uri,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)

    def get_namespace_with_start(self, data):
        self.data = data
        self.ws.on_open = self.on_open
        self.ws.run_forever()
        return self.crypted_auth

    def on_message(self, ws, message):
        try:
            self.crypted_auth = message
        except Exception as e:
            print(e)

    def on_error(self, ws, error):
        if (ws is not None):
            ws.close()
            ws.on_message = None
            ws.on_open = None
            ws.close = None
            del ws
        else:
            print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        json_data = json.dumps(self.data)
        ws.send(json_data)
        pass

if __name__ == "__main__":
    register = ClientRegisterSocket("ws://114.207.113.7:5001")
    namespace = register.get_namespace_with_start({'authkey':'abocd2'})
    print(namespace)
    print(type(namespace))
    auth_uri = urllib.parse.urljoin("ws://114.207.113.7:5001",  namespace)
    auth = ClientAuthSocket(auth_uri)
    auth.ws_comm()
