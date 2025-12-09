from flask import Blueprint, render_template
bp = Blueprint("main", __name__)
@bp.route("/")
def main_menu():
    return render_template("main_menu.html")