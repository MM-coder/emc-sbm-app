import users # Import custom user module 
import passwords # Import custom hashing
import meeting
import proposals
import flask
from flask import Flask, redirect, url_for, render_template, request, session, abort
import hashlib, os


app = Flask(__name__)
app.secret_key = os.urandom(2048)

@app.route('/index')
@app.route('/')
def index():
    if 'logged_in' in session:
        proposals_list = proposals.get_proposals()
        full_name = session['logged_in']['name']
        next_meeting_text = meeting.get_next_meeting_text()
        return render_template('index.html', next_meeting_text = next_meeting_text, display_name = full_name, proposals_list = proposals_list, count = len(proposals_list))
    else:
        return abort(401) # Http 401 error

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.form:
        try:
            password = users.get_user_password(request.form['username'])
            user_obj = users.get_user_object(request.form['username'])
            if password == passwords.hash_plain_text(request.form['password']):
                session['logged_in'] = {"user": request.form['username'], "name": user_obj['full_name']}
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error=True, errortext = "Invalid Username/Password combination! Please try again")
        except:
            return render_template('login.html', error=True, errortext = "We couldn't find that user! Please enter a valid username")
    return render_template('login.html', error=False)


@app.route('/logout')
def logout():
    session.pop('logged_in')
    return redirect(url_for('login'))

@app.errorhandler(401)
def handle_401_error(e):
    return render_template('login.html', error=True, errortext = "You need to be logged in to do that! (HTTP error 401)")


if __name__ == "__main__":
    app.run(debug=True)