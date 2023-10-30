from flask import Flask, render_template
from flask_socketio import SocketIO, send
import redis
import json
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    return render_template('index_websocket.html')

@socketio.on('message')
def handle_message(data):
    if isinstance(data, str):
        data = json.loads(data)
    message = data.get('message')
    sender = data.get('sender')
    if message and sender:
        message_with_sender = {
            "sender": sender,
            "message": message
        }
        r.publish('my-channel', json.dumps(message_with_sender))
        send(message_with_sender, broadcast=True)

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

if __name__ == '__main__':
    threading.Thread(target=subscriber).start()
    socketio.run(app, debug=True)
