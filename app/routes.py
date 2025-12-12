from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from . import db
from .forms import ReservationForm, AdminLoginForm 
from .models import Admin, Reservation
from .utils import ETicketGenerator, calculate_total_sales, get_seat_price
from .crud import (
    verify_admin_credentials,
    get_all_reservations,
    delete_reservation,
    seat_is_taken,
)

bp = Blueprint("main", __name__)

@bp.route('/')
def main_menu():
    return render_template('main_menu.html')

@bp.route('/reserve', methods=['GET', 'POST'])
def reserve_seat():
    form = ReservationForm()
    if form.validate_on_submit():
        row = form.seatRow.data
        col = form.seatColumn.data
        if seat_is_taken(row, col):
            flash(f"Seat Row {row}, Column {col} is already reserved. Please select another seat.", "danger")
            return render_template('reserve_seat.html', form=form)
        generator = ETicketGenerator(length=6)
        eticket = generator.generate()
        new_reservation = Reservation(
            firstName=form.firstName.data,
            lastName=form.lastName.data,
            seatRow=row,
            seatColumn=col,
            eTicketNumber=eticket
        )
        db.session.add(new_reservation)
        db.session.commit()
        return redirect(url_for('main.confirmation', eticket=eticket))
    return render_template('reserve_seat.html', form=form)

@bp.route('/confirmation')
def confirmation():
    eticket = request.args.get('eticket')
    reservation = Reservation.query.filter_by(eTicketNumber=eticket).first()
    if not reservation:
        flash("Reservation details not found.", "warning")
        return redirect(url_for('main.main_menu'))
    return render_template(
        'confirmation.html',
        first_name=reservation.firstName,
        last_name=reservation.lastName,
        row=reservation.seatRow,
        column=reservation.seatColumn,
        eticket=reservation.eTicketNumber
    )


@bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = verify_admin_credentials(form.username.data, form.password.data)
        if admin:
            flash("Logged in successfully.", "success")
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash("Invalid username or password.", "danger")
    if not Admin.query.first():
        return redirect(url_for('main.init_admin'))

    return render_template('admin_login.html', form=form)

@bp.route("/admin/dashboard", methods=["GET"])
def admin_dashboard():
    reservations_db = get_all_reservations()
    total_sales = calculate_total_sales(reservations_db)
    SEAT_ROWS = 12
    SEAT_COLS = 4
    seat_map = [[None] * SEAT_COLS for _ in range(SEAT_ROWS)]
    reservations_for_display = []
    
    for res in reservations_db:
        price = get_seat_price(res.seatRow, res.seatColumn)
        if 1 <= res.seatRow <= SEAT_ROWS and 1 <= res.seatColumn <= SEAT_COLS:
            seat_map[res.seatRow - 1][res.seatColumn - 1] = {
                'id': res.id,
                'name': f"{res.firstName} {res.lastName}",
                'code': res.eTicketNumber,
                'price': price
            }
        reservations_for_display.append({
            'id': res.id,
            'name': f"{res.firstName} {res.lastName}",
            'seat': f"{res.seatRow}{chr(64 + res.seatColumn)}",
            'code': res.eTicketNumber,
            'price': price
        })
    return render_template(
        'admin_dashboard.html',
        reservations=reservations_for_display,
        total_sales=total_sales,
        seat_map=seat_map,
        SEAT_ROWS=SEAT_ROWS,
        SEAT_COLS=SEAT_COLS
    )

@bp.route('/delete/<int:reservation_id>', methods=['POST'])
def delete_reservation_route(reservation_id):
    if delete_reservation(reservation_id):
        flash("Reservation deleted successfully.", "success")
    else:
        flash("Reservation not found.", "danger")
    return redirect(url_for('main.admin_dashboard'))

@bp.route("/admin/init", methods=["GET", "POST"])
def init_admin():
    existing = Admin.query.first()
    if existing:
        flash("Admin already exists.", "warning")
        return redirect(url_for("main.admin_login"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("Please enter both a username and password.", "danger")
            return render_template("init_admin.html")
        hashed_password = generate_password_hash(password)
        admin = Admin(username=username, password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        flash("Admin created successfully! Please log in.", "success")
        return redirect(url_for("main.admin_login"))
    return render_template("init_admin.html")