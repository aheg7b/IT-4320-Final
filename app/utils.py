import random
import string
from .models import Reservation
from . import db
# Import reusable logic and constants from cost_matrix
from .cost_matrix import COST_MATRIX, get_seat_price_by_rowcol, ROWS, COLS

def get_seat_price(row: int, col: int) -> int:
    """Returns the price of a seat at the given row (1-12) and column (1-4)."""
    try:
        # Optimized to use the constant matrix directly
        return get_seat_price_by_rowcol(COST_MATRIX, row, col)
    except (IndexError, ValueError):
        return 0

def calculate_total_sales(reservations: list[Reservation]) -> float:
    """Calculates the total sales collected from a list of reservations (Req G)."""
    # Optimized to use sum with a generator expression directly accessing the helper
    return sum(get_seat_price(res.seatRow, res.seatColumn) for res in reservations)

class ETicketGenerator:
    def __init__(self, length=6):
        self.length = length
        self.characters = string.ascii_uppercase + string.digits

    def generate(self):
        """
        Generate a unique alphanumeric eTicket number.
        Checks the database to avoid duplicates.
        """
        # Add a safety limit to prevent infinite loops (though unlikely)
        for _ in range(100):
            code = ''.join(random.choice(self.characters) for _ in range(self.length))
            # Check if code already exists in DB
            # Use query.scalar() or count() which can be slightly faster than fetching object
            exists = db.session.query(Reservation.id).filter_by(eTicketNumber=code).first() is not None
            if not exists:
                return code
        raise RuntimeError("Failed to generate unique eTicket after 100 attempts")

def format_dashboard_data(reservations: list[Reservation]):
    """
    Process reservations to generate dashboard data:
    - Total sales
    - Seat map structure
    - List of formatted reservation dicts
    """
    total_sales = calculate_total_sales(reservations)
    
    # Initialize seat map
    seat_map = [[None] * COLS for _ in range(ROWS)]
    formatted_reservations = []

    for res in reservations:
        price = get_seat_price(res.seatRow, res.seatColumn)
        
        # Populate seat map if valid seat
        if 1 <= res.seatRow <= ROWS and 1 <= res.seatColumn <= COLS:
            seat_map[res.seatRow - 1][res.seatColumn - 1] = {
                'id': res.id,
                'name': f"{res.firstName} {res.lastName}",
                'code': res.eTicketNumber,
                'price': price
            }
        
        # Add to list
        formatted_reservations.append({
            'id': res.id,
            'name': f"{res.firstName} {res.lastName}",
            'seat': f"{res.seatRow}{chr(64 + res.seatColumn)}", # 65 is A
            'code': res.eTicketNumber,
            'price': price
        })
    
    return {
        'total_sales': total_sales,
        'seat_map': seat_map,
        'formatted_reservations': formatted_reservations,
        'rows': ROWS,
        'cols': COLS
    }

