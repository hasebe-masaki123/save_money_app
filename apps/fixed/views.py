from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from apps.fixed.models import Fixed
from apps.fixed.forms import FixedCreateForm, FixedUpdateForm


fixed_bp = Blueprint(
    'fixed',
    __name__,
    template_folder='templates',
)


# --- 固定費一覧 & 新規登録 ---
@fixed_bp.route('/', methods=['GET', 'POST'])
@login_required
def fixed():

    form = FixedCreateForm()

    # 新規登録
    if form.validate_on_submit():
        new_fixed = Fixed(
            user_id=current_user.user_id,
            name=form.name.data,
            billing_day=form.billing_day.data,
            default_amount=form.default_amount.data,
        )

        db.session.add(new_fixed)
        db.session.commit()

        flash("固定費を登録しました。", "success")
        return redirect(url_for("fixed.fixed"))

    # 一覧表示
    fixed_list = Fixed.query.filter_by(user_id=current_user.user_id).all()

    return render_template("fixed/fixed.html", form=form, fixed_list=fixed_list)


# --- 固定費編集 ---
@fixed_bp.route('/edit/<int:fixed_id>', methods=['GET', 'POST'])
@login_required
def fixed_edit(fixed_id):

    fixed_item = Fixed.query.filter_by(fixed_id=fixed_id, user_id=current_user.user_id).first_or_404()
    form = FixedUpdateForm(obj=fixed_item)

    if form.validate_on_submit():
        fixed_item.name = form.name.data
        fixed_item.billing_day = form.billing_day.data
        fixed_item.default_amount = form.default_amount.data

        db.session.commit()

        flash("固定費を更新しました。", "success")
        return redirect(url_for("fixed.fixed"))

    return render_template("fixed/fixed_edit.html", form=form, fixed_item=fixed_item)
