from flask import Flask, Blueprint, render_template, request, redirect, url_for
import redis
import time
import json

# register page as blueprint
chat_bp = Blueprint('chat', __name__)

# get redis connection
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

# home route is the chatroom
@chat_bp.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # get message from input field
        message = request.form['message']
        # get active user id
        active_user_id = redis.get('active_user_id')
        # get current timestamp
        timestamp = int(time.time())
        # TODO: get actual room ID!!!!
        room_id = '1:2'
        # message for stringified json object
        message_data = {
            'from': active_user_id.decode('utf-8'), 
            'message': message, 
            'timestamp': timestamp,
            'room_id': room_id
        }
        # stringify the json data
        json_data = json.dumps(message_data)
        redis.zadd(f"room:{room_id}", {json_data: timestamp})
    # test
    active_user_id = redis.get('active_user_id')
    return render_template('chat.html', active_user_id=active_user_id.decode('utf-8'))