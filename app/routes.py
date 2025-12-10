from flask import Blueprint, render_template, request
from app import db
from app.models import Admin, Reservation

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

        # Look up admin in the DB
        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.password == password:
            # credentials OK – show admin dashboard
            return render_template("admin_dashboard.html")
        else:
            #  wrong username or password
            error = "Invalid credentials"

    # GET request or failed POST → show login form
    return render_template("admin_login.html", error=error)

@bp.route("/init_admin")
def init_admin():
    # Check if an admin already exists
    existing = Admin.query.first()
    if existing:
        return "Admin already exists."

    # Create a default admin user
    admin = Admin(username="admin", password="admin")
    db.session.add(admin)
    db.session.commit()
    return "Admin created with username=admin, password=admin"

