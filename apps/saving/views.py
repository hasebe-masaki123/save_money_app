from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from apps.saving.models import Saving
from apps.saving.forms import SavingForm


saving_bp = Blueprint(
    'saving', 
    __name__, 
    template_folder='templates',
    static_folder='static',
)



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