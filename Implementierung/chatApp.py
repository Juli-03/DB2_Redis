from flask import Flask, render_template

app = Flask(__name__,static_folder='staticFiles')

# route to registration form
@app.route('/register')
def register():
    return render_template('registration.html')

# route to login form -> is set to default route, so user has always to login first
@app.route('/')
def login():
    return render_template('login.html')

# home route is the chatroom
@app.route('/home')
def home():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)