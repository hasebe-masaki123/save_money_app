import os
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from apps.income.models import Income
from app import db
from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange
 
# --- Blueprint 定義 ---
income_bp = Blueprint(
    'income',
    __name__,
    url_prefix='/income',
    template_folder=os.path.join(os.path.dirname(__file__), 'templates')  # 絶対パス指定
)
 
# --- WTForms ---
class IncomeForm(FlaskForm):
    date = DateField("日付", format="%Y-%m-%d", validators=[DataRequired()])
    amount = IntegerField("金額", validators=[DataRequired(), NumberRange(min=0)])
    memo = TextAreaField("メモ")
    submit = SubmitField("登録")
 
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
 
        flash("収入を登録したさー", "success")
        return redirect(url_for("income.income"))
 
    return render_template("income.html", form=form)  # templatesフォルダ直下なら "income.html"