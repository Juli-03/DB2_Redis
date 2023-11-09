"""
File: chatApp.py
Author: Tim Steiner, Julian Bork, Felix Wilhelm, Marius Wergen
Date: October 13, 2023
Description: This script starts the whole Web Application.

Usage:
- Function main(): Starts the Web Application.

- creates Flask app

- registers blueprints

- runs app
"""

# imports of used libraries
from config import Config
from routes.chat import chat_bp
from routes.login import login_bp
from routes.registration import registration_bp
from flask import Flask, render_template, request, redirect, url_for

# connection to database
pool = Config.pool
redis = Config.redis

# create flask app
app = Flask(__name__,static_folder='staticFiles', template_folder='templates')

# register blueprints
app.register_blueprint(chat_bp)
app.register_blueprint(login_bp)
app.register_blueprint(registration_bp)

# default route = run app
if __name__ == '__main__':
    app.run(debug=True)