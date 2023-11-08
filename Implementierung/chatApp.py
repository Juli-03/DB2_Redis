from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send
from config import Config
from routes.chat import chat_bp
from routes.login import login_bp
from routes.registration import registration_bp

# connection to database
pool = Config.pool
redis = Config.redis

# create flask app
app = Flask(__name__,static_folder='staticFiles', template_folder='templates')
socketio = SocketIO(app)

# register blueprints
app.register_blueprint(chat_bp)
app.register_blueprint(login_bp)
app.register_blueprint(registration_bp)

# default route = run app
if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app, debug=True)