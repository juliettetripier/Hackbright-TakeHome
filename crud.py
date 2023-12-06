from model import db, connect_to_db, User, Reservation

if __name__ == '__main__':
    from server import app
    with app.app_context():
        connect_to_db(app) 


def get_user_by_username(username):
    """Find the user in the DB with the specified username."""

    return User.query.filter_by(username=username).first()