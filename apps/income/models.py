from app import db
from datetime import datetime
from apps.auth.models import User



class Income(db.Model):
    __tablename__ = 'incomes'

    income_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id'),
        nullable=False
    )

    date = db.Column(db.Date)
    amount = db.Column(db.Integer)
    memo = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # リレーション
    user = db.relationship("User", backref="incomes", lazy=True)