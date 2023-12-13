from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db
import crud
from datetime import datetime
import time

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

@app.route('/schedule')
def show_reservation_search():
    if session.get('user'):
        user = crud.get_user_by_id(session.get('user'))
        return render_template('search-form.html',
                               user=user)
    flash('You must log in before viewing this page.')
    return redirect('/')

@app.route('/search')
def show_search_results():
    date = request.args.get('date-picker')
    print(date)
    print(type(date))
    start_time = request.args.get('start-time')
    print(start_time)
    end_time = request.args.get('end-time')
    print(end_time)

    # Convert date string to date object
    converted_date = datetime.strptime(date, '%Y-%m-%d').date()
    print(converted_date)

    # Convert start and end times, if any, to time object
    converted_start_time = datetime.strptime(start_time, '%I:%M').time()
    converted_end_time = datetime.strptime(end_time, '%I:%M').time()
    print(converted_start_time)
    print(converted_end_time)

    # Generate available appointments for this date
    booked_appointments = crud.get_booked_appointments_by_date(date)
    print(booked_appointments)

    # Filter out appointments outside of the specified time range, if any
    if start_time or end_time:
        for appointment in booked_appointments:
            # May need to check for start and end times first
            if appointment.time < converted_start_time:
                print(appointment)
                booked_appointments.remove(appointment)
            if appointment.time > converted_end_time:
                booked_appointments.remove(appointment)

    # Calculate available appointments
    

    return render_template('search-results.html',
                           date=date,
                           start_time=start_time,
                           end_time=end_time,
                           booked_appointments=booked_appointments)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)