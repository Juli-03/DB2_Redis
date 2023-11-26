"""
File: chatApp.py
Author: Tim Steiner, Julian Bork, Felix Wilhelm, Marius Wergen
Date: October 13, 2023
Description: This script starts the whole Web Application.

Usage:
- Function main(): Starts the Web Application.

- creates Flask app

- registers blueprints

- handles storage and redis pubsub 

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

#function that publishes incoming messages in redis pub/sub and saves them in their respectiv rooms 
@socketio.on('message')
def handle_message(data):
    #loads the data received through the websocket
    if isinstance(data, str):
        data = json.loads(data)
    message = data.get('message')
    sender = data.get('user_id')
    timestamp = int(time.time())
    room_id = data.get('room_id')
    #create json to publish and store in redis 
    if message and sender:
        message_with_sender = {
            "user_id": sender,
            "message": message,
            "timestamp": timestamp,
            "room_id": room_id
        }
        #publishing the json in redis pub/sub
        r.publish('all-rooms', json.dumps(message_with_sender))
        #processes json to store in redis db
        json_data = json.dumps(message_with_sender, cls=MessageEncoder)
        #store json with room_id, message with other components in json format and the timestamp
        redis.zadd(f"{room_id}", {json_data: timestamp})

#function that handels the incoming messages from redis pub/sub
def subscriber():
    #initializes redis pub/sub
    pubsub = r.pubsub()
    #subscribes to the pub/sub room
    pubsub.subscribe('all-rooms')
    #listens if any messages have been send to the room
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = message['data']
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            try:
                #loads the received message in the json format
                data = json.loads(data)
                #sends the json to the websocket so it can be shared with the frontend
                socketio.emit('message', data)

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")


if __name__ == '__main__':
    threading.Thread(target=subscriber).start()
    socketio.run(app, debug=True)
