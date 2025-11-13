
from app import db
from datetime import datetime
from flask_login import UserMixin
#ユーザーテーブル
class User(db.Model, UserMixin):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30),nullable=False)
    password_hash = db.Column(db.String(255),nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    
    def get_id(self):
        return str(self.user_id)
