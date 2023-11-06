from flask import Flask, Blueprint, render_template, request, redirect, url_for
from models.room import Room
from models.user import User
from models.message import *
import redis
import time
import json
from config import Config
from loguru import logger

logger.remove()
logger.add("log.log")

# register page as blueprint
chat_bp = Blueprint('chat', __name__)

# get redis connection
redis = redis.StrictRedis(host=Config.host, port=Config.port, db=0)

# home route is the chatroom
@chat_bp.route('/home', methods=['GET', 'POST'])
def home():
    # get user id from url
    user_id = request.args.get('user_id')
    logger.info(f"user_id: {user_id}")
    # get all rooms 
    # Retrieve the user data from Redis
    user_data_json = redis.hget('users', user_id)
    user_data = json.loads(user_data_json.decode('utf-8'))
    # Fetch the "rooms" list from the user data
    room_keys = user_data.get('rooms', [])
    # Initialize an empty list to store the data from sorted sets
    room_data = []
    rooms = []
    selectedRoom = None

    for room_key in room_keys:
        # Retrieve the data from the sorted set
        room_data = redis.zrange(room_key, 0, -1, withscores=True)
        partnerAId = int(room_data[0][0].decode('utf-8'))
        partnerBId = int(room_data[1][0].decode('utf-8'))
        # get both user by their id
        partnerA_data_json = redis.hget('users', partnerAId)
        partnerB_data_json = redis.hget('users', partnerBId)
        partnerA_data = json.loads(partnerA_data_json.decode('utf-8'))
        partnerB_data = json.loads(partnerB_data_json.decode('utf-8'))
        # create User objects for both room partners
        partnerA = User(partnerA_data.get('username', 'Default Name'),partnerA_data.get('email', 'Default Name'), partnerAId)
        partnerB = User(partnerB_data.get('username', 'Default Name'),partnerB_data.get('email', 'Default Name'), partnerBId)
        # create room object and fill it with all values
        tempRoom = Room(partnerA, partnerB, room_key,)
        rooms.append(tempRoom)
        # Append the room data to the list
        room_data.append((room_key, room_data))


    if request.method == 'POST':
        logger.info("POST request")
        # get message from input field
        message = request.form['message']
        # get current timestamp
        timestamp = int(time.time())
        # TODO: get actual room ID!!!!
        room_id = '1:2'
        # message for stringified json object
        message = Message(user_id, message, timestamp, room_id)
        #message_data = {
        #    'from': user_id, 
        #    'message': message, 
        #    'timestamp': timestamp,
        #    'room_id': room_id
        #}
        # stringify the json data
        json_data = json.dumps(message, cls=MessageEncoder)
        #json_data = json.dumps(message_data)
        logger.info(f"json_data: {json_data}")
        redis.zadd(f"room:{room_id}", {json_data: timestamp})
    return render_template('chat.html', user_id=user_id, roomObjects = rooms, selectedRoom = selectedRoom)