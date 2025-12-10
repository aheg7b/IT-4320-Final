# app/crud.py
from app import db
from app.models import Admin, Reservation


# ---------- Admin helpers ----------

def get_admin_by_username(username: str):
    """Return the Admin row for a username, or None."""
    return Admin.query.filter_by(username=username).first()


def verify_admin_credentials(username: str, password: str):
    """
    Return the Admin row if username/password match,
    otherwise return None.
    """
    admin = get_admin_by_username(username)
    if admin and admin.password == password:
        return admin
    return None


# ---------- Reservation helpers ----------

def get_all_reservations():
    """Return a list of all reservations ordered by id."""
    return Reservation.query.order_by(Reservation.id).all()


def seat_is_taken(row: int, col: int) -> bool:
    """Return True if a seat (row, col) already has a reservation."""
    existing = Reservation.query.filter_by(row=row, col=col).first()
    return existing is not None


def create_reservation(first_name: str,
                       last_name: str,
                       row: int,
                       col: int,
                       code: str):
    """
    Create and save a new reservation.
    Returns the created Reservation object.
    """
    reservation = Reservation(
        first_name=first_name,
        last_name=last_name,
        row=row,
        col=col,
        code=code,
    )
    db.session.add(reservation)
    db.session.commit()
    return reservation


def delete_reservation(reservation_id: int) -> bool:
    """
    Delete a reservation by id.
    Returns True if deleted, False if not found.
    """
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return False

    db.session.delete(reservation)
    db.session.commit()
    return True
