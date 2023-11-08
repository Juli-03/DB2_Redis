from flask import Flask, render_template, request, redirect, url_for

from flask_socketio import SocketIO, send
import threading
import redis
import json
import time
from routes.chat import chat_bp, redis

from config import Config
from routes.chat import chat_bp
from routes.login import login_bp
from routes.registration import registration_bp

# connection to database
pool = Config.pool
redis = Config.redis

# create flask app
app = Flask(__name__,static_folder='staticFiles', template_folder='templates')
#create connection to socket and redis server
socketio = SocketIO(app)
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
    if message and sender:
        message_with_sender = {
            "user_id": sender,
            "message": message
        }
        r.publish('my-channel', json.dumps(message_with_sender))
        send(message_with_sender, broadcast=True)
        print(message_with_sender)

def subscriber():
    pubsub = r.pubsub()
    pubsub.subscribe('my-channel')
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = message['data']
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            try:
                data = json.loads(data)
                print(f"Received message from {data['sender']}: {data['message']}")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

# default route = run app
if __name__ == '__main__':
    #app.run(debug=True)
    #threading.Thread(target=subscriber).start()
    threading.Thread(target=subscriber).start()
    socketio.run(app, debug=True)