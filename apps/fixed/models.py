from app import db
from datetime import datetime



class Fixed(db.Model):
    __tablename__ = 'fixeds'


    fixed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    billing_day = db.Column(db.Integer, nullable=False)
    default_amount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class FixedHistory(db.Model):
    __tablename__ = 'fixed_histories'

    fixed_history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fixed_id = db.Column(db.Integer, db.ForeignKey('fixeds.fixed_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    paid_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
