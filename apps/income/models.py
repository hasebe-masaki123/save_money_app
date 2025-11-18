from app import db
from datetime import datetime

class Income(db.Model):
    __tablename__ = 'incomes'

    income_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date      = db.Column(db.Date)
    amount    = db.Column(db.Integer)
    memo      = db.Column(db.Text)
    created_at = db.Column(db.Date, default=datetime.utcnow().date)

    # ユーザーとのリレーション（必要なら）
    user = db.relationship("User", backref="incomes")
