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

    # Set up converted time variables
    converted_start_time = None
    converted_end_time = None

    # Convert date string to date object
    converted_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

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

    # Find booked appointments for this date and remove booked timeslots from list of available timeslots
    booked_appointments = crud.get_booked_appointments_by_date(date)
    print(booked_appointments)
    for appointment in booked_appointments:
        booked_time = appointment.time
        booked_time_string = booked_time.strftime('%H:%M')
        if booked_time_string in time_slots:
            time_slots.remove(booked_time_string)
    print(time_slots)

    # Convert each time slot in list to AM/PM format
    converted_time_slots = []
    for time_slot in time_slots:
        time_slot_object = datetime.datetime.strptime(time_slot, '%H:%M')
        converted_time_slot = time_slot_object.strftime('%I:%M %p')
        converted_time_slots.append(converted_time_slot)



    return render_template('search-results.html',
                           date=date,
                           start_time=start_time,
                           end_time=end_time,
                           time_slots=time_slots,
                           converted_time_slots=converted_time_slots)


@app.route('/book-appointment')
def book_appointment():
    date = request.args.get('date')
    time_slot = request.args.get('time_slot')
    user = session.get('user')

    # Convert date from string to date object
    converted_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    # Check to make sure user doesn't already have an appointment on this date
    appointments_on_date = crud.get_booked_appointments_by_user_and_date(user, date)
    if appointments_on_date:
        flash('You already have an appointment scheduled for this date. Please choose another date.')
    else:
        # Convert time slot from time to time object
        military_time_object = datetime.datetime.strptime(time_slot, '%I:%M %p').time()
        military_time = military_time_object.strftime('%H:%M')
        converted_time = datetime.datetime.strptime(military_time, '%H:%M').time()

        # Add appointment to DB
        crud.create_appointment(date, time_slot, user)
        flash('Appointment booked successfully!')

    return redirect('/user-appointments')


@app.route('/user-appointments')
def show_user_appointments():

    return render_template('user-appointments.html')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)