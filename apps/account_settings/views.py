from flask import Blueprint, render_template, flash, redirect, url_for
from apps.auth.models import User
from apps.account_settings.forms import ChangeEmailForm, ChangePasswordForm
from app import db
from flask_login import login_required,current_user,login_user


account_settings = Blueprint(
    "account_settings",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@account_settings.route("/account_settings", methods=["GET", "POST"])
@login_required
def account_setting():
    return render_template("account_settings/account_settings.html")


@account_settings.route("/change_email", methods=["GET", "POST"])
@login_required
def change_email():
    form = ChangeEmailForm()
    
    if form.validate_on_submit():
        new_email = form.email.data
    
        existing_user = User.query.filter_by(email=new_email).first()
        if existing_user and existing_user.user_id != current_user.user_id:
            flash("このメールアドレスはすでに登録されています。", "warning")
            return redirect(url_for('account_settings.change_email'))
        else:
            current_user.email = new_email
            db.session.commit()
            login_user(current_user, fresh=True)
            return redirect(url_for("account_settings.account_setting"))
    return render_template("account_settings/change_email.html",form=form,email=current_user.email)


@account_settings.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    user = User.query.get(current_user.user_id)
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash("現在のパスワードが間違っています。", "danger")
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            return redirect(url_for("account_settings.account_setting"))

    return render_template("account_settings/change_password.html", form=form)