from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class GoalForm(FlaskForm):
    title = StringField("タイトル", validators=[DataRequired()])
    target_amount = IntegerField("目標金額", validators=[DataRequired(), NumberRange(min=1)])
    deadline_at = DateField("期限", format='%Y-%m-%d', validators=[], default=None)
    submit = SubmitField("登録")