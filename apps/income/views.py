import os
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from apps.income.models import Income
from app import db
from apps.income.forms import IncomeForm


income_bp = Blueprint(
    'income',
    __name__,
    template_folder='templates',
    static_folder='static',
)
 
# --- 収入登録 ---
@income_bp.route("/", methods=["GET", "POST"])
@login_required
def income():
    form = IncomeForm()
 
    if form.validate_on_submit():
        new_income = Income(
            user_id=current_user.user_id,
            date=form.date.data,
            amount=form.amount.data,
            memo=form.memo.data
        )
        db.session.add(new_income)
        db.session.commit()
        
        return redirect(url_for("income.income"))
 
    return render_template("/income/income.html", form=form) 