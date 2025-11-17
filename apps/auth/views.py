from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from apps.auth import auth_bp
from apps.expense import expense_bp
from apps.income import income_bp
from apps.models import User, Expense, ExpenseCategory, Income
from app import db, login_manager
from datetime import datetime
from apps.saving import saving_bp
from apps.models import User, Expense, ExpenseCategory, Income, Saving
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from apps.models import Fixed, FixedCategory
from datetime import datetime




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --------------------
# ログイン
# --------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("ログインしました。", "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash("メールアドレスまたはパスワードが間違っています。", "danger")

    return render_template("auth/login.html")


# --------------------
# サインアップ
# --------------------
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("このメールアドレスはすでに登録されています。", "warning")
            return redirect(url_for("auth.signup"))

        new_user = User(
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        flash("ユーザー登録が完了しました。ログインしてください。", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html")


# --------------------
# ログアウト
# --------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました。", "info")
    return redirect(url_for("auth.login"))


#支出登録
@expense_bp.route('/expense', methods=['GET', 'POST'])
@login_required
def expense():

    categories = ExpenseCategory.query.all()

    if request.method == 'POST':
        date_str = request.form.get("date")
        amount_str = request.form.get("amount")
        category_id = request.form.get("category_id")
        memo = request.form.get("memo")

        if amount_str is None or not amount_str.isdigit() or int(amount_str) < 0:
            flash("0以上の整数を入力してください", "error")
            return redirect(url_for("expense.expense"))

        amount = int(amount_str)

        try:
            expense_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            flash("日付の形式が正しくありません", "error")
            return redirect(url_for("expense.expense"))

        new_expense = Expense(
            user_id=current_user.id,
            category_id=int(category_id),
            date=expense_date,
            amount=amount,
            memo=memo
        )

        db.session.add(new_expense)
        db.session.commit()

        flash("支出を登録しました", "success")
        return redirect(url_for("expense.expense"))

    return render_template("expense/expense.html", categories=categories)



#支出カテゴリ登録
@expense_bp.route("/add_category", methods=["POST"])
@login_required
def add_category():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": "カテゴリ名が必要です"}), 400

    existing = ExpenseCategory.query.filter_by(name=name).first()
    if existing:
        return jsonify({"id": existing.category_id, "name": existing.name})

    new_cat = ExpenseCategory(name=name)
    db.session.add(new_cat)
    db.session.commit()

    return jsonify({"id": new_cat.category_id, "name": new_cat.name})



# 収入登録
@income_bp.route("/income", methods=["GET", "POST"])
@login_required
def income():

    if request.method == "POST":
        date_str = request.form.get("date")
        amount_str = request.form.get("amount")
        memo = request.form.get("memo")

        if amount_str is None or not amount_str.isdigit() or int(amount_str) < 0:
            flash("0以上の整数を入力してください", "error")
            return redirect(url_for("income.income"))

        amount = int(amount_str)

        try:
            income_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            flash("日付の形式が正しくありません", "error")
            return redirect(url_for("income.income"))

        new_income = Income(
            user_id=current_user.id,
            date=income_date,
            amount=amount,
            memo=memo
        )

        db.session.add(new_income)
        db.session.commit()

        flash("収入を登録しました", "success")
        return redirect(url_for("income.income"))

    return render_template("income/income.html")


@saving_bp.route("/saving", methods=["GET", "POST"])
@login_required
def saving():

    if request.method == "POST":
        date_str = request.form.get("date")
        amount_str = request.form.get("amount")
        memo = request.form.get("memo")

        # --- 金額チェック ---
        if amount_str is None or not amount_str.isdigit() or int(amount_str) < 0:
            flash("0以上の整数を入力してください", "error")
            return redirect(url_for("saving.saving"))

        amount = int(amount_str)

        # --- 日付チェック ---
        try:
            saving_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            flash("正しい形式で入力してください", "error")
            return redirect(url_for("saving.saving"))

        # --- DBへ保存 ---
        new_saving = Saving(
            user_id=current_user.id,
            date=saving_date,
            amount=amount,
            memo=memo
        )

        db.session.add(new_saving)
        db.session.commit()

        flash("貯金を登録しました", "success")
        return redirect(url_for("saving.saving"))

    return render_template("saving/saving.html")





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