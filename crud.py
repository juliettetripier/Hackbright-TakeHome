from model import db, connect_to_db, User, Reservation

if __name__ == '__main__':
    from server import app
    with app.app_context():
        connect_to_db(app) 


def get_user_by_username(username):
    """Find the user in the DB with the specified username."""

    return User.query.filter_by(username=username).first()

def get_user_by_id(user_id):
    """Find the user in the DB with the specified user ID."""

    return User.query.get(user_id)

def get_booked_appointments_by_date(appt_date):
    """Find all booked appointments on a given date."""

    return Reservation.query.filter_by(date=appt_date).all()

def get_booked_appointments_by_user(user_id):
    """Find all booked appointments for a given user."""

    return Reservation.query.filter_by(user_id=user_id).all()

def get_booked_appointments_by_user_and_date(user_id, date):
    """Find all booked appointments for a given user on a given date."""

    return Reservation.query.filter_by(user_id=user_id, date=date).all()

def create_appointment(date, time_slot, user_id):
    """Add an appointment with the specified user, date, and time slot to the DB."""

    new_appointment = Reservation(user_id=user_id, date=date, time_slot=time_slot)
    db.session.add(new_appointment)
    db.session.commit()
