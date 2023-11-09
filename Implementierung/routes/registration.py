from flask import Flask, Blueprint, render_template, request, redirect, url_for
import redis
import json
from config import Config
from loguru import logger
import bcrypt

logger.remove()
logger.add("log.log")

# register page as blueprint
registration_bp = Blueprint('registration', __name__)

# get redis connection
redis = redis.StrictRedis(host=Config.host, port=Config.port, db=0)

# route to registration form
@registration_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # TODO perform validation
        
        # get user info from input fields
        reg_email = request.form['reg_email']
        reg_username = request.form['reg_username']
        reg_password = request.form['reg_password']
        reg_password_repeat = request.form['reg_password_repeat'] 
        # hash the password
        salt = bcrypt.gensalt() # generate salt -> number of rounds of hashing (default: 12)
        reg_password_hash = bcrypt.hashpw(reg_password.encode('utf-8'), salt) #returns a byte object
        reg_password_hash = reg_password_hash.decode('utf-8') # convert byte object to string
        logger.info(f"Password: {reg_password}, reg_password_hash: {reg_password_hash}")
        error = ""
        
        # Check if the passwords match
        if reg_password != reg_password_repeat:
            # If registration is not successful, redirect the user to the "register" route
            error+="M"
            #return redirect(url_for('registration.register', error="M")) #error M for mismatch
        else:
            logger.info("Passwords match")

        # Check if the user id counter already exists
        if not redis.exists('user_id_counter'):
            # If the key does not exist, initialize it with a default value
            redis.set('user_id_counter', 0)
        # user id counter already exists
        else:
            # check if email already exists
            user_id = redis.zscore("user_emails", reg_email)
            # email already exists
            if user_id is not None:
                error+="E"
                # If registration is not successful, redirect the user to the "register" route
                #return redirect(url_for('registration.register', error="E")) #error E for email already exists
                
        if error!="":
            #if error occured redirect to registration page with error code
            return redirect(url_for('registration.register', error=error))
        # get an avatar for the user
        avatar_index = int(redis.get('user_id_counter')) % 8
        # get new user id (increment user_id_counter by 1)
        reg_user_id = redis.incr('user_id_counter')

        # Add the email to the ZSET with the user_id as the score
        redis.zadd("user_emails", {reg_email: reg_user_id})

        # save user data in form of a json object
        logger.warning(f"typeof reg_password_hash: {type(reg_password_hash)}")
        user_data = {
            'email': reg_email,
            'username': reg_username,
            'password': reg_password_hash,
            'rooms': [],
            'avatar': avatar_index
        }
        # save user data in redis db as stringified json object
        redis.hset("users", reg_user_id, json.dumps(user_data))

        # Get all user IDs from the Redis hash set
        user_ids = redis.hkeys('users')

        # Iterate over the user IDs
        for user_id_iter in user_ids:
            if not user_id_iter.decode('utf-8') == str(reg_user_id):
                room_name = f"room:{user_id_iter.decode('utf-8')}:{reg_user_id}"
                # Create an empty sorted set with no members
                redis.zadd(room_name, {reg_user_id: -1})
                redis.zadd(room_name, {user_id_iter: -2})
                user_data_iter_json_bytes = redis.hget('users', user_id_iter.decode('utf-8'))
                user_data_iter_json = json.loads(user_data_iter_json_bytes)
                user_data_iter_json['rooms'].append(room_name)
                redis.hset('users', user_id_iter, json.dumps(user_data_iter_json))
                # add the room to the room list of the user
                user_data['rooms'].append(room_name)
                # Update the user's data in Redis
                redis.hset('users', reg_user_id, json.dumps(user_data))

        # If registration is successful, redirect the user to the "home" route
        return redirect(url_for('chat.home', user_id=reg_user_id))
    else:
        return render_template('registration.html')
