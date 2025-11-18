from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from apps.models import Fixed, FixedCategory




fixed_bp = Blueprint('fixed', __name__, url_prefix='/fixed')
# 固定費登録
@fixed_bp.route('/', methods=['GET', 'POST'])
@login_required
def fixed():
    categories = FixedCategory.query.all()

    if request.method == 'POST':
        date_str = request.form.get("date")
        amount_str = request.form.get("amount")
        category_id = request.form.get("category_id")

        # 金額チェック
        if amount_str is None or not amount_str.isdigit() or int(amount_str) < 0:
            flash("0以上の整数を入力してください", "error")
            return redirect(url_for("fixed.fixed"))

        amount = int(amount_str)

        # 日付チェック
        try:
            fixed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            flash("日付の形式が正しくありません", "error")
            return redirect(url_for("fixed.fixed"))

        # DBに保存
        new_fixed = Fixed(
            user_id=current_user.id,
            category_id=int(category_id),
            amount=amount,
            date=fixed_date
        )

        db.session.add(new_fixed)
        db.session.commit()

        flash("固定費を登録しました", "success")
        return redirect(url_for("fixed.fixed"))

    return render_template("fixed/fixed.html", categories=categories)


# 固定費カテゴリ
@fixed_bp.route('/fixedcategory', methods=['GET', 'POST'])
@login_required
def fixed_category():
    # カテゴリ一覧取得
    categories = FixedCategory.query.all()

    if request.method == 'POST':
        name = request.form.get("name")

        # 空文字チェック
        if not name or name.strip() == "":
            flash("カテゴリ名を入力してください", "error")
            return redirect(url_for("fixed.fixed_category"))

        # 既に同名カテゴリが無いかチェック
        existing = FixedCategory.query.filter_by(name=name).first()
        if existing:
            flash("同じ名前のカテゴリがすでに存在します", "error")
            return redirect(url_for("fixed.fixed_category"))

        # DB追加
        new_category = FixedCategory(name=name)
        db.session.add(new_category)
        db.session.commit()

        flash("カテゴリを追加しました", "success")
        return redirect(url_for("fixed.fixed_category"))

    return render_template("fixed/category.html", categories=categories)
