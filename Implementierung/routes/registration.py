from flask import Flask, Blueprint, render_template, request, redirect, url_for
import redis
import json

# register page as blueprint
registration_bp = Blueprint('registration', __name__)

# get redis connection
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

# route to registration form
@registration_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # TODO perform validation
        
        # get user info from input fields
        reg_email = request.form['reg_email']
        reg_username = request.form['reg_username']
        reg_password = request.form['reg_password']

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
                # If registration is not successful, redirect the user to the "register" route
                # TODO: show error message
                return redirect(url_for('registration.register'))

        # get new user id (increment user_id_counter by 1)
        reg_user_id = redis.incr('user_id_counter')

        # Add the email to the ZSET with the user_id as the score
        redis.zadd("user_emails", {reg_email: reg_user_id})
        
        # save user data in form of a json object
        user_data = {
            'email': reg_email,
            'username': reg_username,
            'password': reg_password,
            'rooms': [room:1:2, ]
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
                redis.zadd(room_name, {'initial_message': -1})

        # If registration is successful, redirect the user to the "home" route
        return redirect(url_for('chat.home', user_id=reg_user_id))
    else:
        return render_template('registration.html')
