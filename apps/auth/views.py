from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from apps.auth.models import User
from app import db, login_manager
from apps.auth.forms import LoginForm, SignUpForm

auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("ログインしました。", "success")
            return redirect(url_for("top.top"))
        else:
            flash("メールアドレスまたはパスワードが間違っています。", "danger")

    return render_template("auth/login.html", form=form)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        password_confirm = form.password_confirm.data

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

    return render_template("auth/signup.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました。", "info")
    return redirect(url_for("auth.login"))
