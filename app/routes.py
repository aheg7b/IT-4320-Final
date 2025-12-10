from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app import db
from app.models import Admin, Reservation
from app.crud import (
    verify_admin_credentials,
    get_all_reservations,
    delete_reservation,
    create_reservation,
    seat_is_taken,
)

bp = Blueprint("main", __name__)

@bp.route("/")
def main_menu():
    return render_template("main_menu.html")

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