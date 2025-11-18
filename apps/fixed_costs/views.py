from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from apps.models import Fixed, FixedCategory
 
# ===== Flask-WTF =====
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange
 
 
fixed_bp = Blueprint('fixed', __name__, url_prefix='/fixed')
 
 
# ============================
#        フォーム定義
# ============================
 
# 固定費登録フォーム
class FixedForm(FlaskForm):
    date = DateField('日付', validators=[DataRequired()])
    amount = IntegerField('金額', validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField('カテゴリ', coerce=int, validators=[DataRequired()])
    submit = SubmitField('登録')
 
 
# カテゴリ追加フォーム
class FixedCategoryForm(FlaskForm):
    name = StringField('カテゴリ名', validators=[DataRequired()])
    submit = SubmitField('追加')
 
 
# ============================
#        固定費登録
# ============================
 
@fixed_bp.route('/', methods=['GET', 'POST'])
@login_required
def fixed():
 
    categories = FixedCategory.query.all()
 
    form = FixedForm()
    form.category_id.choices = [(c.category_id, c.name) for c in categories]
 
    if form.validate_on_submit():
 
        new_fixed = Fixed(
            user_id=current_user.id,
            category_id=form.category_id.data,
            amount=form.amount.data,
            date=form.date.data,
        )
 
        db.session.add(new_fixed)
        db.session.commit()
 
        flash("固定費を登録しました", "success")
        return redirect(url_for("fixed.fixed"))
 
    return render_template("fixed/fixed.html", form=form)
 
 
# ============================
#        固定費カテゴリ登録
# ============================
 
@fixed_bp.route('/fixedcategory', methods=['GET', 'POST'])
@login_required
def fixed_category():
 
    categories = FixedCategory.query.all()
    form = FixedCategoryForm()
 
    if form.validate_on_submit():
 
        # 同名カテゴリチェック
        existing = FixedCategory.query.filter_by(name=form.name.data).first()
        if existing:
            flash("同じ名前のカテゴリがすでに存在します", "error")
            return redirect(url_for("fixed.fixed_category"))
 
        new_category = FixedCategory(name=form.name.data)
        db.session.add(new_category)
        db.session.commit()
 
        flash("カテゴリを追加しました", "success")
        return redirect(url_for("fixed.fixed_category"))
 
    return render_template("fixed/category.html", form=form, categories=categories)