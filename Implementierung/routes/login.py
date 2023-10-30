from flask import Flask, Blueprint, render_template, request, redirect, url_for
import redis

# register page as blueprint
login_bp = Blueprint('login', __name__)

# get redis connection
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

# route to login form -> is set to default route, so user has always to login first
@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # TODO perform validation
        # get entered email and password
        email = request.form['email']
        password = request.form['password']
        # save email and password of active user in redis db
        redis.set('active_email', email)
        redis.set('active_password', password)
        # If login is successful, redirect the user to the "home" route
        return redirect(url_for('chat.home'))
    else:
        return render_template('login.html')