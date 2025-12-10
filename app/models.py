# app/models.py
from app import db

class Reservation(db.Model):
    __tablename__ = "reservations"   

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    row = db.Column(db.Integer, nullable=False)
    col = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<Reservation {self.first_name} {self.last_name} seat=({self.row},{self.col})>"


class Admin(db.Model):
    __tablename__ = "admins"  

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)  

    def __repr__(self):
        return f"<Admin {self.username}>"
