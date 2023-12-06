from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db
import crud

app = Flask(__name__)
app.secret_key = "placeholder"

@app.route('/')
def show_homepage():
    return render_template('homepage.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')

    user = crud.get_user_by_username(username)

    if user:
        session['user'] = user.user_id
        session['username'] = user.username
        return redirect('/landingpage')
    flash('Username invalid. Please try again')
    return redirect('/')

@app.route('/landingpage')
def show_landing_page():
    if session.get('user'):
        return render_template('landingpage.html')
    flash('You must log in before viewing this page.')
    return redirect('/')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)