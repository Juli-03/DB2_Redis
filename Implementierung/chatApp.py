from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__,static_folder='staticFiles')

# route to registration form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process the form data here
        # Perform registration and any necessary validation

        # If registration is successful, redirect the user to the "home" route
        return redirect(url_for('home'))
    else:
        return render_template('registration.html')

# route to login form -> is set to default route, so user has always to login first
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process the form data here
        # Perform login and any necessary validation

        # If login is successful, redirect the user to the "home" route
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

# home route is the chatroom
@app.route('/home')
def home():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)