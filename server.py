from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db
import crud
import datetime
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
    start_time = request.args.get('start-time')
    end_time = request.args.get('end-time')

    # Set up converted date and time variables
    converted_date = None
    converted_start_time = None
    converted_end_time = None

    # Convert date string to date object
    if date:
        converted_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    # Convert start and end times, if any, to time object
    if start_time:
        converted_start_time = datetime.datetime.strptime(start_time, '%H:%M').time()
    if end_time:
        converted_end_time = datetime.datetime.strptime(end_time, '%H:%M').time()

    # Generate appointment slots for this date
    time_slots = []
    if start_time:
        current_time = datetime.datetime.strptime(start_time, '%H:%M').time()
    else:
        current_time = datetime.datetime.strptime('0:00', '%H:%M').time()
    current_time_datetime = datetime.datetime.combine(converted_date, current_time)
    if end_time:
        end = datetime.datetime.strptime(end_time, '%H:%M').time()
    else:
        end = datetime.datetime.strptime('23:30', '%H:%M').time()
    end_datetime = datetime.datetime.combine(converted_date, end)

    while current_time_datetime <= end_datetime:
        time_slots.append((current_time_datetime).strftime('%H:%M'))
        current_time_datetime += datetime.timedelta(minutes=30)
    print(time_slots)

    # Find booked appointments for this date
    booked_appointments = crud.get_booked_appointments_by_date(date)
    print(booked_appointments)



    # This actually doesn't make sense.
    # I need to rewrite this so we generate appointment slots
    # remove the slots which are already booked
    # and THEN filter out appointments by time
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