from flask import Flask, Blueprint, render_template, request, redirect, url_for
import redis

# register page as blueprint
chat_bp = Blueprint('chat', __name__)

# get redis connection
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

# home route is the chatroom
@chat_bp.route('/home')
def home():
    # test
    email = redis.get('active_email')
    return render_template('chat.html', active_email=email.decode('utf-8'))