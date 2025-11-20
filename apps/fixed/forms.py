from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


# --- 固定費マスタ：新規登録 ---
class FixedCreateForm(FlaskForm):
    name = StringField('固定費名', validators=[DataRequired()])
    billing_day = IntegerField('請求日', validators=[DataRequired(), NumberRange(min=1, max=31)])
    default_amount = IntegerField('金額', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('追加')


# --- 固定費マスタ：編集 ---
class FixedUpdateForm(FlaskForm):
    name = StringField('固定費名', validators=[DataRequired()])
    billing_day = IntegerField('請求日', validators=[DataRequired(), NumberRange(min=1, max=31)])
    default_amount = IntegerField('金額', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('更新')
