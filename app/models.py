from datetime import datetime
from app import db


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    passengerName = db.Column(db.String, nullable=False)
    seatRow = db.Column(db.Integer, nullable=False)
    seatColumn = db.Column(db.Integer, nullable=False)
    eTicketNumber = db.Column(db.String, nullable=False, unique=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return (
            f"<Reservation {self.passengerName} "
            f"seat=({self.seatRow},{self.seatColumn}) code={self.eTicketNumber}>"
        )


class Admin(db.Model):
    __tablename__ = "admins"

    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Admin {self.username}>"
