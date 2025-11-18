from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from apps.expense import expense_bp
from apps.models import Expense, ExpenseCategory
from app import db
from datetime import datetime


#支出登録
@expense_bp.route('/expense', methods=['GET', 'POST'])
@login_required
def expense():

    categories = ExpenseCategory.query.all()

    if request.method == 'POST':
        date_str = request.form.get("date")
        amount_str = request.form.get("amount")
        category_id = request.form.get("category_id")
        memo = request.form.get("memo")

        if amount_str is None or not amount_str.isdigit() or int(amount_str) < 0:
            flash("0以上の整数を入力してください", "error")
            return redirect(url_for("expense.expense"))

        amount = int(amount_str)

        try:
            expense_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            flash("日付の形式が正しくありません", "error")
            return redirect(url_for("expense.expense"))

        new_expense = Expense(
            user_id=current_user.id,
            category_id=int(category_id),
            date=expense_date,
            amount=amount,
            memo=memo
        )

        db.session.add(new_expense)
        db.session.commit()

        flash("支出を登録しました", "success")
        return redirect(url_for("expense.expense"))

    return render_template("expense/expense.html", categories=categories)



#支出カテゴリ登録
@expense_bp.route("/add_category", methods=["POST"])
@login_required
def add_category():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": "カテゴリ名が必要です"}), 400

    existing = ExpenseCategory.query.filter_by(name=name).first()
    if existing:
        return jsonify({"id": existing.category_id, "name": existing.name})

    new_cat = ExpenseCategory(name=name)
    db.session.add(new_cat)
    db.session.commit()

    return jsonify({"id": new_cat.category_id, "name": new_cat.name})