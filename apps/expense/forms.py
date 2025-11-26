from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, HiddenField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length
from datetime import date


class ExpenseForm(FlaskForm):

    date = DateField(
        "日付",
        format='%Y-%m-%d',
        validators=[DataRequired()],
        default=date.today(),  # ← 呼び出しに修正
    )

    amount = IntegerField(
        "金額",
        validators=[
            DataRequired(),
            NumberRange(min=1),  # ← 1円以上の支出
        ],
    )

    memo = StringField(
        "メモ",
        validators=[
            Length(max=100),  # ← Length に修正
        ],
    )

    # ボタン選択用（非表示で値を受け取る）
    category_id = HiddenField(
        validators=[DataRequired("カテゴリを選択してください")],
    )

    submit = SubmitField("登録")


class ExpenseCategoryForm(FlaskForm):
    name = StringField(
        "カテゴリ名",
        validators=[
            DataRequired("カテゴリ名を入力してください"),
            Length(min=1, max=20),
        ],
    )

    submit = SubmitField("追加")
