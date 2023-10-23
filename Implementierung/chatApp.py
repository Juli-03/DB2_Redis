from flask import Flask, render_template

app = Flask(__name__,static_folder='staticFiles')

@app.route('/')
def home():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)