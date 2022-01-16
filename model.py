import datetime
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()


class Reservation(db.Model):
    __tablename__ = "reservations"

    reservation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String)
    start_time = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<User username={self.username} start_time={self.start_time}>"

    def to_dict(self):
        return {
            "reservation_id": self.reservation_id,
            "username": self.username,
            "start_time": self.start_time.isoformat(),
        }

    @classmethod
    def find_reservation_by_start_and_user(cls, reservation_start, username):
        reservation_to_delete = (
            cls.query.filter(Reservation.start_time == reservation_start)
            .filter(Reservation.username == username)
            .first()
        )
        return reservation_to_delete

    @classmethod
    def get_all_for_user(cls, username):
        return cls.query.filter_by(username=username).all()

    @classmethod
    def new_reservation_for_user(cls, username, reservation_start):
        return cls(username=username, start_time=reservation_start)

    @classmethod
    def find_available_reservations(cls, start_time, end_time, username):
        # retrieve reservations in within the specified time range
        all_reservations_in_range = db.session.query(cls.start_time).filter(
            cls.start_time.between(start_time, end_time)
        )
        # get reservation times without time zone
        existing_reservation_times = {
            res[0].replace(tzinfo=None) for res in all_reservations_in_range.all()
        }

        # of existing reservations, get the ones with the user
        user_reservations = all_reservations_in_range.filter(
            cls.username == username
        ).all()
        user_reservation_dates = {res.start_time.date() for res in user_reservations}

        # Initialize list for possible times
        times = []

        # Possible reservations can only happen on the half hour
        first_reservation_time = start_time + (datetime.min - start_time) % timedelta(
            minutes=30
        )
        current = first_reservation_time

        # Add possible times, filtering where a reservation already exists OR where
        # user already has a reservation on that date
        while current < end_time:
            if (
                current not in existing_reservation_times
                and current.date() not in user_reservation_dates
            ):
                times.append(current)
            current = current + timedelta(minutes=30)
        return times


def connect_to_db(flask_app):
    db_uri = os.environ["DATABASE_URL"].replace("postgres", "postgresql")
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    app = Flask(__name__)
    connect_to_db(app)
