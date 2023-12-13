from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
        autoincrement=True,
        primary_key=True)
    username = db.Column(db.String, unique=True)

class Reservation(db.Model):
    """A reservation."""

    __tablename__ = "reservations"

    reservation_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    date = db.Column(db.Date)
    time = db.Column(db.Time)


def connect_to_db(flask_app, db_uri="postgresql:///melons", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)