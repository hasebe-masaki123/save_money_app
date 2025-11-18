from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from models import Saving
from forms import SavingForm
 
saving_bp = Blueprint('saving', __name__)
 
# --- 貯金登録 ---
@saving_bp.route('/saving/add', methods=['GET', 'POST'])
@login_required
def add_saving():
    form = SavingForm()
 
    if form.validate_on_submit():
        new_saving = Saving(
            user_id=current_user.id,
            date=form.date.data,
            amount=form.amount.data,
            memo=form.memo.data,
            created_at=datetime.now()
        )
 
        db.session.add(new_saving)
        db.session.commit()
 
        flash('貯金を登録しました', 'success')
        return redirect(url_for('saving.add_saving'))  # 必要なら一覧ページに変更
 
    return render_template('saving/add.html', form=form)