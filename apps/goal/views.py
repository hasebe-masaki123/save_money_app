from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from apps.models import Goal
import Blueprint, render_template, request, redirect, url_for, flash

# 目標管理用Blueprint
goal_bp = Blueprint('goal', __name__, url_prefix='/goals')

# 目標一覧
@goal_bp.route('/')
@login_required
def index():
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template('goals/index.html', goals=goals)

# 目標登録（GET/POST）
@goal_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        target_amount = request.form.get('target_amount')
        deadline_at = request.form.get('deadline_at')

        # 入力チェック
        if not title or not target_amount:
            flash('タイトルと目標金額は必須です', 'error')
            return redirect(url_for('goal.create'))

        try:
            target_amount = int(target_amount)
        except ValueError:
            flash('目標金額は整数で入力してください', 'error')
            return redirect(url_for('goal.create'))

        if deadline_at:
            try:
                deadline_at = datetime.strptime(deadline_at, '%Y-%m-%d').date()
            except ValueError:
                flash('日付の形式が正しくありません', 'error')
                return redirect(url_for('goal.create'))
        else:
            deadline_at = None

        goal = Goal(
            user_id=current_user.id,
            title=title,
            target_amount=target_amount,
            current_amount=0,
            deadline_at=deadline_at,
            created_at=datetime.now(),
            updated_at=None,
        )

        db.session.add(goal)
        db.session.commit()

        flash('目標を登録しました', 'success')
        return redirect(url_for('goal.index'))

    return render_template('goals/create.html') 
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from apps.models import Goal

# 目標管理用Blueprint
goal_bp = Blueprint('goal', __name__, url_prefix='/goals')

# 目標一覧
@goal_bp.route('/')
@login_required
def index():
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template('goals/index.html', goals=goals)

# 目標登録（GET/POST）
@goal_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        target_amount = request.form.get('target_amount')
        deadline_at = request.form.get('deadline_at')

        # 入力チェック
        if not title or not target_amount:
            flash('タイトルと目標金額は必須です', 'error')
            return redirect(url_for('goal.create'))

        try:
            target_amount = int(target_amount)
        except ValueError:
            flash('目標金額は整数で入力してください', 'error')
            return redirect(url_for('goal.create'))

        # 日付が空ならNone
        if deadline_at:
            try:
                deadline_at = datetime.strptime(deadline_at, '%Y-%m-%d').date()
            except ValueError:
                flash('日付の形式が正しくありません', 'error')
                return redirect(url_for('goal.create'))
        else:
            deadline_at = None

        # データ登録
        goal = Goal(
            user_id=current_user.id,
            title=title,
            target_amount=target_amount,
            current_amount=0,
            deadline_at=deadline_at,
            created_at=datetime.now(),
            updated_at=None,
        )

        db.session.add(goal)
        db.session.commit()

        flash('目標を登録しました', 'success')
        return redirect(url_for('goal.index'))

    return render_template('goals/create.html')
