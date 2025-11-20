from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from apps.expense.models import Expense, ExpenseCategory
from app import db
from datetime import datetime

# --- expense 用 Blueprint ---
expense_bp = Blueprint("expense", __name__, url_prefix="/expense", template_folder="templates")

@expense_bp.route("/", methods=["GET", "POST"])
@login_required
def expense():
    categories = ExpenseCategory.query.all()

    if request.method == "POST":
        date_str = request.form.get("date")
        amount_str = request.form.get("amount")
        category_input = request.form.get("category_id")
        memo = request.form.get("memo")

        # 金額チェック
        if amount_str is None or not amount_str.isdigit() or int(amount_str) < 0:
            flash("0以上の整数を入力してね", "error")
            return redirect(url_for("expense.expense"))

        amount = int(amount_str)

        # 日付チェック
        try:
            expense_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            flash("日付の形式が正しくないさー", "error")
            return redirect(url_for("expense.expense"))

        # カテゴリIDの処理
        if category_input.isdigit():
            category_id = int(category_input)
        else:
            existing = ExpenseCategory.query.filter_by(name=category_input).first()
            if existing:
                category_id = existing.category_id
            else:
                new_category = ExpenseCategory(name=category_input)
                db.session.add(new_category)
                db.session.commit()
                category_id = new_category.category_id

        new_expense = Expense(
            user_id=current_user.user_id,
            category_id=category_id,
            date=expense_date,
            amount=amount,
            memo=memo
        )
        db.session.add(new_expense)
        db.session.commit()

        flash("支出を登録したさー", "success")
        return redirect(url_for("expense.expense"))

    return render_template("expense/expense.html", categories=categories)


@expense_bp.route("/add_category", methods=["POST"])
@login_required
def add_category():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": "カテゴリ名を入力してください"}), 400

    existing = ExpenseCategory.query.filter_by(name=name).first()
    if existing:
        return jsonify({"id": existing.category_id, "name": existing.name})

    new_cat = ExpenseCategory(name=name)
    db.session.add(new_cat)
    db.session.commit()

    return jsonify({"id": new_cat.category_id, "name": new_cat.name})


@expense_bp.route("/total", methods=["GET"])
@login_required
def total_expense():
    total = db.session.query(db.func.sum(Expense.amount)).filter_by(user_id=current_user.user_id).scalar()
    if total is None:
        total = 0
    return jsonify({"total": total})


@expense_bp.route("/total_by_category", methods=["GET"])
@login_required
def total_by_category():
    results = db.session.query(
        ExpenseCategory.name,
        db.func.sum(Expense.amount)
    ).join(ExpenseCategory, Expense.category_id == ExpenseCategory.category_id) \
     .filter(Expense.user_id == current_user.user_id) \
     .group_by(ExpenseCategory.name).all()
    data = [{"category": r[0], "total": r[1]} for r in results]
    return jsonify(data)


@expense_bp.route("/by_date", methods=["GET"])
@login_required
def expense_by_date():
    start_str = request.args.get("start")
    end_str = request.args.get("end")
    try:
        start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
    except:
        return jsonify({"error": "日付形式が正しくないさー"}), 400

    expenses = Expense.query.filter(
        Expense.user_id == current_user.user_id,
        Expense.date >= start_date,
        Expense.date <= end_date
    ).all()

    data = [
        {"date": e.date.strftime("%Y-%m-%d"), "amount": e.amount, "category_id": e.category_id, "memo": e.memo}
        for e in expenses
    ]
    return jsonify(data)


# --- menu 用 Blueprint ---
menu_bp = Blueprint("menu", __name__, url_prefix="", template_folder="templates")

@menu_bp.route("/menu/", methods=["GET"])
# @login_required
def input_menu_page():
    return render_template("input_select.html")
