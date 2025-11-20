from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from apps.goal.models import Goal
from apps.goal.forms import GoalForm

goal_bp = Blueprint(
    'goal',
    __name__,
    template_folder='templates',
)


@goal_bp.route('/')
@login_required
def index():
    goal = Goal.query.filter_by(user_id=current_user.user_id).first()
    return render_template('goal/goal_setting.html', goal=goal)


@goal_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = GoalForm()

    # すでに目標があるか取得（あっても1件）
    existing_goal = Goal.query.filter_by(user_id=current_user.user_id).first()

    # POST（送信）時
    if form.validate_on_submit():

        # deadline は任意入力
        deadline_value = form.deadline_at.data

        if existing_goal:
            # --- 既存目標がある → UPDATE ---
            existing_goal.title = form.title.data
            existing_goal.target_amount = form.target_amount.data
            # 現在の金額は維持する（仕様に応じて変更可能）
            existing_goal.deadline_at = deadline_value

            flash("目標を更新しました", "success")

        else:
            # --- 初めての登録 → INSERT ---
            new_goal = Goal(
                user_id=current_user.user_id,
                title=form.title.data,
                target_amount=form.target_amount.data,
                current_amount=0,
                deadline_at=deadline_value,
            )
            db.session.add(new_goal)
            flash("目標を登録しました", "success")

        db.session.commit()
        return redirect(url_for('goal.index'))

    # GET（初期表示）時
    # すでにある目標をフォームに反映するとユーザーに優しい
    if existing_goal and not form.is_submitted():
        form.title.data = existing_goal.title
        form.target_amount.data = existing_goal.target_amount
        form.deadline_at.data = existing_goal.deadline_at

    return render_template('goal/add_goal.html', form=form)
