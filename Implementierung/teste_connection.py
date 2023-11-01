from flask import Flask, render_template, request, redirect, url_for
import redis

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    return render_template('index.html', keys=r.keys('*'))

@app.route('/get/<key>')
def get_key(key):
    value = r.get(key)
    return f"Key: {key}, Value: {value.decode('utf-8') if value else 'Key not found'}"

@app.route('/set', methods=['POST'])
def set_key():
    key = request.form['key']
    value = request.form['value']
    r.set(key, value)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
