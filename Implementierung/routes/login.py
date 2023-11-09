# library imports
import json
import redis
import bcrypt
import requests
from PIL import Image
from io import BytesIO
from loguru import logger
from config import Config
from flask import Flask, Blueprint, render_template, request, redirect, url_for

# urls where the avatars are stored
avatar_urls = ["https://bootdey.com/img/Content/avatar/avatar1.png",
            "https://bootdey.com/img/Content/avatar/avatar2.png",
            "https://bootdey.com/img/Content/avatar/avatar3.png",
            "https://bootdey.com/img/Content/avatar/avatar4.png",
            "https://bootdey.com/img/Content/avatar/avatar5.png",
            "https://bootdey.com/img/Content/avatar/avatar6.png",
            "https://bootdey.com/img/Content/avatar/avatar7.png",
            "https://bootdey.com/img/Content/avatar/avatar8.png"]

logger.remove()
logger.add("log.log")
# register page as blueprint
login_bp = Blueprint('login', __name__)

# get redis connection
redis = redis.StrictRedis(host=Config.host, port=Config.port, db=0)

# route to login form -> is set to default route, so user has always to login first
@login_bp.route('/', methods=['GET', 'POST'])
def login():
    # check if the avatar images have already been loaded into the database
    if not redis.exists('avatars'):
        # load avatars into database
        # iterate over all 8 avatar urls
        for index, img_url in enumerate(avatar_urls):
            # create a byte stream
            output = BytesIO()
            # open the image from the url
            im = Image.open(BytesIO(requests.get(img_url).content))
            # save the image in the byte stream
            im.save(output, format=im.format)
            # add the image to the database
            redis.zadd("avatars", {output.getvalue(): index})
            # close the byte stream
            output.close()

    # Method if the user clicks the "Login" button
    if request.method == 'POST':
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
            try:
                user_id = int(redis.zscore("user_emails", email))
            except(TypeError):
                logger.info("email does not exist")
                user_id = None
            # email does not exist -> user has to register first
            if user_id is None:
                # TODO: show error message
                return redirect(url_for('login.login', error="True"))
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
                if bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8')):
                    # If login is successful, redirect the user to the "home" route
                    logger.info(f"login successful for user_id: {user_id}")
                    return redirect(url_for('chat.home', user_id=user_id))
                # If login is not successful, redirect the user to the "login" route
                else:
                    logger.info("login not successful")
                    return redirect(url_for('login.login', error="True"))
    else:
        return render_template('login.html')