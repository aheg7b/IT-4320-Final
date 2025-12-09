from flask import Blueprint, render_template
bp = Blueprint("main", __name__)
@bp.route("/")
def main_menu():
    return render_template("main_menu.html")
@bp.route("/reserve")
def reserve_seat():
    return render_template("reserve_seat.html")
@bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if "POST" == str(request.method):
        username = request.form.get("username")
        password = request.form.get("password")
        # For now, allow only admin/admin
        #THIS IS WHERE WE WILL ADD LOGIC FOR LOGIN
        if username == "admin" and password == "admin":
            return render_template("admin_dashboard.html")
        else:
            error = "Invalid credentials"
            return render_template("admin_login.html", error=error)
    return render_template("admin_login.html")