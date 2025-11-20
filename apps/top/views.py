from flask import Blueprint, render_template, url_for
from flask_login import current_user

top_bp = Blueprint(
    "top",
    __name__,
    template_folder="templates",
)

@top_bp.route("/")
def top():
    return render_template("top/top.html")