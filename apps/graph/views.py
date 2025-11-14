# views.py

from flask import Blueprint, render_template, request, jsonify
from .utils import get_current_month_str
from .services import get_weekly_and_total

graph = Blueprint("graph", __name__, template_folder="templates")


@graph.route("/")
def index():
    month = get_current_month_str()
    week_labels, weekly_data, total_data = get_weekly_and_total(month)

    return render_template(
        "graph/graphs.html",
        current_month=month,
        week_labels=week_labels,
        weekly_data=weekly_data,
        total_data=total_data
    )


@graph.route("/weekly-data")
def weekly_data_api():
    month = request.args.get("month")
    week_labels, weekly_data, total_data = get_weekly_and_total(month)

    return jsonify({
        "week_labels": week_labels,
        "weekly": weekly_data,
        "total": total_data
    })
