from app import db
from datetime import datetime
from apps.auth.models import User

# 貯金テーブル
class Saving(db.Model):
    __tablename__ = 'saving'

    saving_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 貯金ID
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id'),
        nullable=False
    )  # ユーザーID
    date = db.Column(db.Date, nullable=False)  # 貯金日
    amount = db.Column(db.Integer, nullable=False)  # 金額
    memo = db.Column(db.Text)  # メモ
    created_at = db.Column(db.DateTime, default=datetime.now)  # 登録日時

    # --- リレーション（ユーザーと紐づけ） ---
    user = db.relationship('User', backref='savings', lazy=True)