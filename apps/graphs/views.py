# views.py
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from .utils import get_current_month_str
from .demo_services import get_weekly_and_total
from datetime import datetime


graphs_bp = Blueprint(
    "graphs",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@login_required
@graphs_bp.route("/")
def index():
    current_month = datetime.now().strftime("%Y-%m")
    # 初期表示は支出(expense)
    week_labels, weekly, total = get_weekly_and_total(current_month, "expense")

    return render_template(
        "graphs/graphs.html",
        current_month=current_month,
        week_labels=week_labels,
        weekly_data=weekly,
        total_data=total
    )


@graphs_bp.route("/data")
def data_api():
    month = request.args.get("month")
    mode = request.args.get("mode")
    week_labels, weekly, total = get_weekly_and_total(month, mode)

    return jsonify({
        "week_labels": week_labels,
        "weekly": weekly,
        "total": total
    })