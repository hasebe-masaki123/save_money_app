from app import db
from datetime import datetime

#ユーザーテーブル
class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30),nullable=False)
    password = db.Column(db.String(128),nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)