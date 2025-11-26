from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from apps.expense.models import Expense, ExpenseCategory
from apps.expense.forms import ExpenseForm, ExpenseCategoryForm
from app import db

# --- expense 用 Blueprint ---
expense_bp = Blueprint(
    "expense", 
    __name__, 
    template_folder="templates",
    static_folder="static",
    )

@expense_bp.route("/", methods=["GET", "POST"])
@login_required
def expense():
    form = ExpenseForm()
    categories = ExpenseCategory.query.all()

    if form.validate_on_submit():
        new_expense = Expense(
            user_id=current_user.user_id,
            amount=form.amount.data,
            date=form.date.data,
            category_id=form.category_id.data,
            memo=form.memo.data
        )
        print("1")
        db.session.add(new_expense)
        db.session.commit()
        flash("支出を記録しました", "success")

        return redirect(url_for("expense.expense"))
    print("2")
    return render_template("expense/expense.html", form=form, categories=categories)


@expense_bp.route("/categories", methods=["GET"])
@login_required
def category_list():
    categories = ExpenseCategory.query.all()
    return render_template("expense/category_list.html", categories=categories)


@expense_bp.route("/add_category", methods=["GET","POST"])
@login_required
def add_category():
    form = ExpenseCategoryForm()

    if form.validate_on_submit():
        new_category = ExpenseCategory(
            name=form.name.data
        )
        db.session.add(new_category)
        db.session.commit()
        flash("カテゴリを追加しました", "success")
        return redirect(url_for("expense.expense"))
    
    return render_template("expense/add_category.html", form=form)

