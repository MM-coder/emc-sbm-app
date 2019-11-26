import users # Import custom user module 
import flask
from flask import Flask, redirect, url_for, render_template, request, session
import hashlib


app = Flask(__name__)
app.secret_key = b"74 a7 62 83 f4 82 ca b1 78 34"

@app.route('/index')
@app.route('/')
def index():
    return "Hi"

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.form:
        try:
            password = users.get_user_password(request.form['username'])
            if password == request.form['password']:
                session['logged_in'] = {"user": request.form['username']}
        except:
            pass
        
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)