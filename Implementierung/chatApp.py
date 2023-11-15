"""
File: chatApp.py
Author: Tim Steiner, Julian Bork, Felix Wilhelm, Marius Wergen
Date: October 13, 2023
Description: This script starts the whole Web Application.

Usage:
- Function main(): Starts the Web Application.

- creates Flask app

- registers blueprints

- runs app
"""

# imports of used libraries
from config import Config
from routes.chat import chat_bp
from routes.login import login_bp
from routes.registration import registration_bp
from flask import Flask, render_template, request, redirect, url_for

from flask_socketio import SocketIO, send
import threading
import redis
import json
import time
from routes.chat import redis
from models.message import *

# connection to database
pool = Config.pool
redis = Config.redis

# create flask app
app = Flask(__name__,static_folder='staticFiles', template_folder='templates')
#create connection to socket and redis server
socketio = SocketIO(app, async_mode = 'threading')
r = redis

# register blueprints
app.register_blueprint(chat_bp)
app.register_blueprint(login_bp)
app.register_blueprint(registration_bp)

#functions for pubishing and subscribing i´with redis and websocket
@socketio.on('message')
def handle_message(data):
    if isinstance(data, str):
        data = json.loads(data)
    message = data.get('message')
    sender = data.get('user_id')
    timestamp = int(time.time())
    room_id = data.get('room_id')
    
    if message and sender:
        message_with_sender = {
            "user_id": sender,
            "message": message,
            "timestamp": timestamp,
            "room_id": room_id
        }
        r.publish('all-rooms', json.dumps(message_with_sender))
        #send(message_with_sender, broadcast=True)
        json_data = json.dumps(message_with_sender, cls=MessageEncoder)
        redis.zadd(f"{room_id}", {json_data: timestamp})
        print(message_with_sender)

def subscriber():
    pubsub = r.pubsub()
    pubsub.subscribe('all-rooms')
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = message['data']
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            try:
                data = json.loads(data)
                print(f"Received message from {data['user_id']}: {data['message']}")
                socketio.emit('message', data)
                print("send data over to socket: ", data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

# default route = run app
if __name__ == '__main__':
    #app.run(debug=True)
    #threading.Thread(target=subscriber).start()
    threading.Thread(target=subscriber).start()
    socketio.run(app, debug=True)



# Überlegung:    Schreiben der historischen Chats auch über den Websocket