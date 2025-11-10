from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, regexp


class SignUpForm(FlaskForm):
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired(""),
            Email(""),
            regexp('^[a-zA-Z0-9_]+$', message='英数字とアンダースコアのみ使用できます。'),
        ],
    )
    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired(""),
            Length(min=8, message='パスワードは8文字以上で入力してください。'),
            regexp('^[a-zA-Z0-9_]+$', message='英数字とアンダースコアのみ使用できます。'),
        ],
        )
    confirm_password = PasswordField(
        "パスワード（確認用）",
        validators=[
            DataRequired(""),
            EqualTo('password', message='パスワードが一致しません。'),
            regexp('^[a-zA-Z0-9_]+$', message='英数字とアンダースコアのみ使用できます。'),
        ],
        )
    submit = SubmitField("サインアップ")


class LoginForm(FlaskForm):
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired(""),
            Email(""),
            regexp('^[a-zA-Z0-9_]+$', message='英数字とアンダースコアのみ使用できます。'),
        ],
    )
    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired(""),
            Length(min=8, message='パスワードは8文字以上で入力してください。'),
            regexp('^[a-zA-Z0-9_]+$', message='英数字とアンダースコアのみ使用できます。'),
        ],
    )
    submit = SubmitField("ログイン")

    
    