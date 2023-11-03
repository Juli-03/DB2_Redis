from flask import Flask, Blueprint, render_template, request, redirect, url_for
import redis
import json
from config import Config
from loguru import logger

logger.remove()
logger.add("logs/login.log")
# register page as blueprint
login_bp = Blueprint('login', __name__)

# get redis connection
redis = redis.StrictRedis(host=Config.host, port=Config.port, db=0)

# route to login form -> is set to default route, so user has always to login first
@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # TODO perform validation
        # get entered email and password
        email = request.form['email']
        password = request.form['password']

        # Check if the user id counter already exists
        if not redis.exists('user_id_counter'):
            # there are no users in database
            return redirect(url_for('login.login'))
        # user id counter already exists
        else:
            # check if email already exists
            user_id = int(redis.zscore("user_emails", email))
            # email does not exist -> user has to register first
            if user_id is None:
                # TODO: show error message
                return redirect(url_for('login.login'))
            # email exists -> check password
            else:
                # get user data from database as json object
                user_data_json = redis.hget("users", user_id)
                if user_data_json is not None:
                    # convert json object to python dictionary
                    user_data = json.loads(user_data_json)
                # get password from database
                db_password = user_data['password']
                # compare entered password with database
                if password == db_password:
                    # If login is successful, redirect the user to the "home" route
                    logger.info(f"login successful for user_id: {user_id}")
                    return redirect(url_for('chat.home', user_id=user_id))
                # If login is not successful, redirect the user to the "login" route
                else:
                    return redirect(url_for('login.login'))
    else:
        return render_template('login.html')