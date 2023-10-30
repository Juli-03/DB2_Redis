from flask import Flask, Blueprint, render_template, request, redirect, url_for
import redis

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
        reg_user_id = redis.incr('user_id_counter')
        reg_email = request.form['reg_email']
        reg_username = request.form['reg_username']
        reg_password = request.form['reg_password']

        # create HSET
        redis.hset(f'user:{reg_user_id}', 'email', reg_email)
        redis.hset(f'user:{reg_user_id}', 'username', reg_username)
        redis.hset(f'user:{reg_user_id}', 'password', reg_password)

        # save email and password of active user in redis db
        redis.set('active_email', reg_email)
        redis.set('active_password', reg_password)

        # If registration is successful, redirect the user to the "home" route
        return redirect(url_for('chat.home'))
    else:
        return render_template('registration.html')