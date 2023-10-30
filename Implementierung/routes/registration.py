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
        reg_email = request.form['reg_email']
        reg_username = request.form['reg_username']
        reg_password = request.form['reg_password']

        # get number of users from database
        number_of_users = redis.get('user_id_counter')

        # loop through all users
        for user_id in range(1, int(number_of_users) + 1):
            # get email from database
            db_email = redis.hget(f'user:{user_id}', 'email')

            # compare entered email and password with database
            # check if account already exists
            if reg_email == db_email.decode('utf-8'):
                # If registration is not successful, redirect the user to the "register" route
                # TODO: show error message
                return redirect(url_for('registration.register'))

        reg_user_id = redis.incr('user_id_counter')

        # create HSET
        redis.hset(f'user:{reg_user_id}', 'email', reg_email)
        redis.hset(f'user:{reg_user_id}', 'username', reg_username)
        redis.hset(f'user:{reg_user_id}', 'password', reg_password)

        # save active user id in redis db
        redis.set('active_user_id', reg_user_id)

        # If registration is successful, redirect the user to the "home" route
        return redirect(url_for('chat.home'))
    else:
        return render_template('registration.html')
