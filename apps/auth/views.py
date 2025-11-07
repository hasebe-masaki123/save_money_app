from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from apps.auth import auth_bp
from apps.models import User
from app import db, login_manager



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました。", "info")
    return redirect(url_for("auth.login"))
