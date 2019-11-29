import users # Import custom user module 
import passwords # Import custom hashing
import meetings
import proposals
import flask
from flask import Flask, redirect, url_for, render_template, request, session, abort, send_file
import hashlib, os


app = Flask(__name__)
app.secret_key = os.urandom(2048)


def checklogin():
    if 'logged_in' in session:
        return True
    else:
        return abort(401)



@app.route('/index')
@app.route('/')
def index():
    checklogin()
    proposals_list = proposals.get_proposals()
    full_name = session['logged_in']['name']
    next_meeting_text = meetings.get_next_meeting_text()
    last_meeting_obg = meetings.get_last_meeting_info()
    return render_template('index.html', next_meeting_text = next_meeting_text, display_name = full_name, proposals_list = proposals_list, count = len(proposals_list), teachers = last_meeting_obg['meeting_teachers'], students = last_meeting_obg['meeting_students'], topics_listed = last_meeting_obg['topics_listed'], topics_covered = last_meeting_obg['topics_covered'], meeting_date = last_meeting_obg['meeting_date'])

@app.route('/resources')
def resources():
    checklogin()
    full_name = session['logged_in']['name']
    templates_list = os.listdir('files/templates')
    return render_template('resources.html', display_name = full_name, templates_list = templates_list, proposals_list = os.listdir('files/proposals'), logs_list = os.listdir('files/logs').remove('ignore.txt'))

@app.route('/about')
def about():
    checklogin()
    full_name = session['logged_in']['name']
    return render_template('about.html', display_name = full_name)




@app.route('/login', methods=["GET", "POST"])
def login():
    if request.form:
        try:
            user_obj = users.get_user_object(request.form['username'])
            if user_obj['password'] == passwords.hash_plain_text(request.form['password']):
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


# File Downloading API


@app.route('/api/download_template/<path>')
def download_template(path):
        if path != None:
            try:
                return send_file('files/templates/' + path, as_attachment=True)
            except:
                return abort(500)
        else:
            return abort(404)

@app.route('/api/download_log/<path>')
def download_log(path):
        if path != None:
            try:
                return send_file('files/logs/' + path, as_attachment=True)
            except:
                return abort(500)
        else:
            return abort(404)

@app.route('/api/download_proposal/<path>')
def download_proposal(path):
        if path != None:
            try:
                return send_file('files/proposals/' + path, as_attachment=True)
            except:
                return abort(500)
        else:
            return abort(404)

@app.errorhandler(401)
def handle_401_error(e):
    return render_template('login.html', error=True, errortext = "You need to be logged in to do that! (HTTP error 401)")


if __name__ == "__main__":
    app.run()