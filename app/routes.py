from flask import Blueprint, render_template
bp = Blueprint("main", __name__)
@bp.route("/")
def main_menu():
    return render_template("main_menu.html")
@bp.route("/reserve")
def reserve_seat():
    return render_template("reserve_seat.html")