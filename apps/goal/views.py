from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from apps.models import Goal
 
# Flask-WTF
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange
 
 
# =========================================
#  Flask-WTF フォーム定義
# =========================================
 
class GoalForm(FlaskForm):
    title = StringField("タイトル", validators=[DataRequired()])
    target_amount = IntegerField("目標金額", validators=[DataRequired(), NumberRange(min=1)])
    deadline_at = DateField("期限", format='%Y-%m-%d', validators=[], default=None)
    submit = SubmitField("登録")
 
 
# =========================================
#  Blueprint 設定
# =========================================
 
goal_bp = Blueprint('goal', __name__, url_prefix='/goals')
 
 
# =========================================
#  目標一覧
# =========================================
@goal_bp.route('/')
@login_required
def index():
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template('goals/index.html', goals=goals)
 
 
# =========================================
#  目標登録（GET/POST）
# =========================================
@goal_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = GoalForm()
 
    # POST & バリデーション成功
    if form.validate_on_submit():
 
        # deadline は任意入力 → 空なら None になるのでそのままでOK
        deadline_value = form.deadline_at.data
 
        new_goal = Goal(
            user_id=current_user.id,
            title=form.title.data,
            target_amount=form.target_amount.data,
            current_amount=0,
            deadline_at=deadline_value,
            created_at=datetime.now(),
            updated_at=None,
        )
 
        db.session.add(new_goal)
        db.session.commit()
 
        flash("目標を登録しました", "success")
        return redirect(url_for('goal.index'))
 
    # 初期表示（GET）
    return render_template('goals/create.html', form=form)