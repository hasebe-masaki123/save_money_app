from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from apps.auth.models import User
from apps.auth.services import authenticate_user, create_user, is_email_registered
from app import login_manager
from apps.auth.forms import LoginForm, SignUpForm

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate_user(form.email.data, form.password.data)

        if user:
            login_user(user)
            flash("ログインしました。", "success")
            return redirect(url_for("top.top"))

        flash("メールアドレスまたはパスワードが間違っています。", "danger")

    return render_template("auth/login.html", form=form)



@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data

        if is_email_registered(email):
            flash("このメールアドレスはすでに登録されています。", "warning")
            return redirect(url_for("auth.signup"))

        create_user(email, form.password.data)
        flash("ユーザー登録が完了しました。ログインしてください。", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html", form=form)



@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました。", "info")
    return redirect(url_for("auth.login"))