"""
File: chat.py
Author: Tim Steiner, Julian Bork, Felix Wilhelm, Marius Wergen
Date: October 13, 2023
Description: This script contains the routes for the chatroom.

Usage:
- Function home(): Renders the chat.html template.

- Function getRoom(): Returns a Room object with all data from the room.

- Function clickedRoom(): Renders the chat.html template with the selected room.
"""

# imports of used libraries
import time
import json
import redis
from config import Config
from loguru import logger
from models.room import Room
from models.user import User
from models.message import *
from datetime import datetime
from flask import Flask, Blueprint, jsonify, render_template, request, redirect, url_for

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
        tempRoom = getRoom(room_key)
        rooms.append(tempRoom)
        # Append the room data to the list
        room_data.append((room_key, room_data))
    return render_template('chat.html', user_id=user_id, roomObjects = rooms, selectedRoom = selectedRoom)

# route to render the chatroom when a room is clicked
@chat_bp.route('/getClickedRoom', methods=['POST','GET'])
def clickedRoom():
    roomId = request.args.get('roomId')
    selectedRoom = getRoom(roomId)
    user_id = request.args.get('userId')
    # Retrieve the user data from Redis
    user_data_json = redis.hget('users', user_id)
    user_data = json.loads(user_data_json.decode('utf-8'))
    # Fetch the "rooms" list from the user data
    room_keys = user_data.get('rooms', [])
    # Initialize an empty list to store the data from sorted sets
    rooms = []
    for room_key in room_keys:
        tempRoom = getRoom(room_key)
        rooms.append(tempRoom)

    # handle send message
    if request.method == 'POST':
        logger.info("POST request")
        # get message from input field
        message = request.form['message']
        # get current timestamp
        timestamp = int(time.time())
        sender_data = redis.hget('users', user_id)
        sender_json = json.loads(sender_data.decode('utf-8'))
        avatarSender = redis.zrangebyscore("avatars", sender_json['avatar'], sender_json['avatar'])
        sender = User(sender_json.get('username', 'Default Name'),sender_json.get('email', 'Default Name'), user_id, avatarSender)
        # message for stringified json object
        message = Message(user_id, message, timestamp, roomId,sender)
        # stringify the json data
        json_data = json.dumps(message, cls=MessageEncoder)
        #json_data = json.dumps(message_data)
        logger.info(f"json_data: {json_data}")
        redis.zadd(f"{roomId}", {json_data: timestamp})
    # Render the chat.html template with the updated selectedRoom
    return render_template('chat.html', user_id=user_id, roomObjects=rooms, selectedRoom=selectedRoom)

# help function to get all data from a room
def getRoom(room_key):
         # Retrieve the data from the sorted set
        room_data = redis.zrange(room_key, 0, -1, withscores=True)
        partnerAId = int(room_data[0][0].decode('utf-8'))
        partnerBId = int(room_data[1][0].decode('utf-8'))
        # get both user by their id
        partnerA_data_json = redis.hget('users', partnerAId)
        partnerB_data_json = redis.hget('users', partnerBId)
        partnerA_data = json.loads(partnerA_data_json.decode('utf-8'))
        partnerB_data = json.loads(partnerB_data_json.decode('utf-8'))

        #avatarA = redis.zscore("avatars", partnerA_data['avatar'])
        avatarA = redis.zrangebyscore("avatars", partnerA_data['avatar'], partnerA_data['avatar'])
        avatarB = redis.zrangebyscore("avatars", partnerB_data['avatar'], partnerB_data['avatar'])
        #avatarB = redis.zscore("avatars", partnerB_data['avatar'])

        # create User objects for both room partners
        # HIER USER BILD EINFÜGEN
        partnerA = User(partnerA_data.get('username', 'Default Name'),partnerA_data.get('email', 'Default Name'), partnerAId, avatarA)
        partnerB = User(partnerB_data.get('username', 'Default Name'),partnerB_data.get('email', 'Default Name'), partnerBId, avatarB)
        messages = []
        # get all messages from the room
        for index in room_data[2:]:
            messageJSON = json.loads(index[0].decode('utf-8'))
            # convert the time
            time_object = datetime.fromtimestamp(messageJSON['timestamp'])
            # Format the datetime object as a string
            formatted_time = time_object.strftime('%d/%m/%Y, %H:%M:%S')
            sender_data = redis.hget('users', messageJSON['user_id'])
            sender_json = json.loads(sender_data.decode('utf-8'))
            avatarSender = redis.zrangebyscore("avatars", sender_json['avatar'], sender_json['avatar'])
            sender = User(sender_json.get('username', 'Default Name'),sender_json.get('email', 'Default Name'), messageJSON['user_id'], avatarSender)
            tempMessage = Message(messageJSON['user_id'],messageJSON['message'],formatted_time, messageJSON['room_id'],sender)
            messages.append(tempMessage)
        # create room object and fill it with all values
        tempRoom = Room(partnerA, partnerB, room_key,messages)
        return tempRoom