from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app import app, db
from app.forms import ReservationForm
from app.models import Admin, Reservation
from app.utils import generate_reservation_code
from app.crud import (
    verify_admin_credentials,
    get_all_reservations,
    delete_reservation,
    create_reservation,
    seat_is_taken,
)

bp = Blueprint("main", __name__)

@app.route('/reserve', methods=['GET', 'POST'])
def reserve_seat():
    form = ReservationForm()
    if form.validate_on_submit():
        reservation_code = generate_reservation_code()
        new_reservation = Reservation(
            name=form.name.data,
            seat_number=form.seat_number.data,
            code=reservation_code
        )
        db.session.add(new_reservation)
        db.session.commit()
        return render_template('confirmation.html', code=reservation_code, name=form.name.data, seat=form.seat_number.data)
    return render_template('reserve_seat.html', form=form)

@bp.route("/reserve")
def reserve_seat():
    return render_template("reserve_seat.html")

@bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin = verify_admin_credentials(username, password)
        if admin:
            # For now, just load dashboard after login
            reservations = get_all_reservations()
            return render_template(
                "admin_dashboard.html",
                admin=admin,
                reservations=reservations,
                total_sales=0,  # we'll calculate this properly later
            )
        else:
            error = "Invalid credentials"
            
    return render_template("admin_login.html", error=error)

@bp.route("/init_admin", methods=["GET", "POST"])
def init_admin():
    # Check if an admin already exists
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
        admin = Admin(username=username, password=generate_password_hash(password))
        db.session.add(admin)
        db.session.commit()
        flash("Admin created successfully!", "success")
        return redirect(url_for("main.admin_login"))
    return render_template("init_admin.html")

@bp.route("/admin/add", methods=["POST"])
def add_admin():
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        flash("Please provide both username and password.", "danger")
        return redirect(url_for("main.admin_login"))
    existing = Admin.query.filter_by(username=username).first()
    if existing:
        flash("Username already exists.", "warning")
        return redirect(url_for("main.admin_login"))
    admin = Admin(username=username, password=generate_password_hash(password))
    db.session.add(admin)
    db.session.commit()
    flash(f"Admin '{username}' created successfully!", "success")
    return redirect(url_for("main.admin_login"))