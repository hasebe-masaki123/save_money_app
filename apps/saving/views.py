from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from apps.saving.models import Saving

# WTForms
from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange

# --- Blueprint ---
saving_bp = Blueprint('saving', __name__, url_prefix='/saving', template_folder='templates')

# --- フォーム ---
class SavingForm(FlaskForm):
    date = DateField("日付", format="%Y-%m-%d", validators=[DataRequired()])
    amount = IntegerField("金額", validators=[DataRequired(), NumberRange(min=0)])
    memo = TextAreaField("メモ")
    submit = SubmitField("登録")

# --- 貯金登録 (ルートを / に変更) ---
@saving_bp.route("/", methods=["GET", "POST"])
@login_required
def saving():
    form = SavingForm()

    if form.validate_on_submit():
        new_saving = Saving(
            user_id=current_user.user_id,
            date=form.date.data,
            amount=form.amount.data,
            memo=form.memo.data,
            created_at=datetime.now()
        )
        db.session.add(new_saving)
        db.session.commit()

        flash("貯金を登録しました", "success")
        return redirect(url_for("saving.add_saving"))

    return render_template("saving/saving.html", form=form)
