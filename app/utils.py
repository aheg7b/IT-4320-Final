import random
import string
from .models import Reservation
from . import db

def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix

def get_seat_price(row: int, col: int) -> int:
    """Returns the price of a seat at the given row (1-12) and column (1-4)."""
    matrix = get_cost_matrix()
    try:
        if not (1 <= row <= 12 and 1 <= col <= 4):
            return 0
        return matrix[row - 1][col - 1]
    except IndexError:
        return 0

def calculate_total_sales(reservations: list[Reservation]) -> float:
    """Calculates the total sales collected from a list of reservations (Req G)."""
    total = 0.0
    for res in reservations:
        price = get_seat_price(res.seatRow, res.seatColumn)
        total += price
    return total

class ETicketGenerator:
    def __init__(self, length=6):
        self.length = length
        self.characters = string.ascii_uppercase + string.digits

    def generate(self):
        """
        Generate a unique alphanumeric eTicket number.
        Checks the database to avoid duplicates.
        """
        while True:
            code = ''.join(random.choice(self.characters) for _ in range(self.length))
            # Check if code already exists in DB
            existing = Reservation.query.filter_by(eTicketNumber=code).first()
            if not existing:
                return code