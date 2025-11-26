from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class ChangeEmailForm(FlaskForm):
    email = StringField(
        "新しいメールアドレス",
        validators=[
            DataRequired(),
            Email(message="有効なメールアドレスを入力してください")
        ],
    )
    submit = SubmitField("確定")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "現在のパスワード",
        validators=[DataRequired()]
    )
    new_password = PasswordField(
        "新しいパスワード",
        validators=[
            DataRequired(),
            Length(min=8, message='パスワードは8文字以上で入力してください')
        ]
    )
    password_confirm = PasswordField(
        "パスワード（確認用）",
        validators=[
            DataRequired(),
            EqualTo('new_password', message='パスワードが一致しません')
        ]
    )
    submit = SubmitField("確定")