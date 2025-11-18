from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from apps.income import income_bp
from apps.models import Income
from app import db
from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange
 

class IncomeForm(FlaskForm):
    date = DateField("日付", format="%Y-%m-%d", validators=[DataRequired()])
    amount = IntegerField("金額", validators=[DataRequired(), NumberRange(min=0)])
    memo = TextAreaField("メモ")
    submit = SubmitField("登録")
 

@income_bp.route("/income", methods=["GET", "POST"])
@login_required
def income():
    form = IncomeForm()
 
    if form.validate_on_submit():
        # データベースに保存
        new_income = Income(
            user_id=current_user.id,
            date=form.date.data,
            amount=form.amount.data,
            memo=form.memo.data
        )
        db.session.add(new_income)
        db.session.commit()
 
        flash("収入を登録しました", "success")
        return redirect(url_for("income.income"))
 
    return render_template("income/income.html", form=form)