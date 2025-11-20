from app import db
from datetime import date

#固定費テーブル
class Fixed(db.Model):
    __tablename__ = 'fixed'

    fixed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 固定費ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ユーザーID
    category_id = db.Column(db.Integer, db.ForeignKey('fixed_categories.id'), nullable=False)  # 固定費カテゴリID
    amount = db.Column(db.Integer, nullable=False)  # 金額
    date = db.Column(db.Date, default=date.today)  # 支払日

    # --- リレーション ---
    # user = db.relationship('User', backref='fixeds', lazy=True)
    # category = db.relationship('FixedCategory', backref='fixeds', lazy=True)

#固定費カテゴリテーブル
class FixedCategory(db.Model):
    __tablename__ = 'fixed_categories'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 固定費カテゴリID
    name = db.Column(db.String(30), nullable=False)  # カテゴリ名

    # --- 関連（固定費テーブルとの紐づけ） ---
    fixeds = db.relationship('Fixed', backref='category', lazy=True)