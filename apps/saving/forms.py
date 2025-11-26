from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange, length
from datetime import date

class SavingForm(FlaskForm):
    date = DateField(
        "日付",
        format='%Y-%m-%d',
        validators=[DataRequired()],
        default=date.today(),
    )

    amount = IntegerField(
        "金額",
        validators=[
            DataRequired(),
            NumberRange(min=0),
        ],
    )

    memo = StringField(
        "メモ",
        validators=[
            length(max=100),
        ],
    )

    submit = SubmitField("登録")