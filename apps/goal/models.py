from app import db
from datetime import datetime

class Goal(db.Model):
    __tablename__ = 'goal'

    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    target_amount = db.Column(db.Integer, nullable=False)
    current_amount = db.Column(db.Integer, nullable=False, default=0)
    deadline_at = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime)