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

        # get number of users from database
        number_of_users = redis.get('user_id_counter')

        # loop through all users
        for user_id in range(1, int(number_of_users) + 1):
            # get email and password from database
            db_email = redis.hget(f'user:{user_id}', 'email')
            db_password = redis.hget(f'user:{user_id}', 'password')

            # compare entered email and password with database
            if email == db_email.decode('utf-8') and password == db_password.decode('utf-8'):
                # save active user id in redis db
                redis.set('active_user_id', user_id)
                # If login is successful, redirect the user to the "home" route
                return redirect(url_for('chat.home'))
        # If login is not successful, redirect the user to the "login" route
        # TODO: show error message
        return redirect(url_for('login.login'))
    else:
        return render_template('login.html')