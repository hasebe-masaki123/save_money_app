# views.py
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from .services import get_weekly_and_total, get_six_months_summary
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
    mode = request.args.get("mode", "expense")  # デフォルトは支出
    
    # モードによって表示形式を自動決定
    if mode == "expense":
        # 支出は週別表示（現在月のデータ）
        labels, data, total = get_weekly_and_total(current_month, mode)
        view_type = "weekly"
    else:
        # 収入と貯金は6か月表示（現在月を基準とする過去6か月）
        labels, data, total = get_six_months_summary(mode, current_month)
        view_type = "monthly"

    return render_template(
        "graphs/graphs.html",
        current_month=current_month,
        labels=labels,
        data=data,
        total_data=total,
        view_type=view_type,
        mode=mode
    )


@graphs_bp.route("/data")
def data_api():
    month = request.args.get("month")
    mode = request.args.get("mode", "expense")
    
    # モードによって表示形式を自動決定
    if mode == "expense":
        # 支出は週別表示（選択月のデータ）
        labels, data, total = get_weekly_and_total(month, mode)
        view_type = "weekly"
    else:
        # 収入と貯金は6か月表示（選択月を基準とする過去6か月）
        labels, data, total = get_six_months_summary(mode, month)
        view_type = "monthly"


    return jsonify({
        "labels": labels,
        "data": data,
        "total": total,
        "view_type": view_type
    })
