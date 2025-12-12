import random
import string
from .models import Reservation
from . import db

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
