from app import db
from datetime import date

#支出テーブル
class Expense(db.Model):
    __tablename__ = 'expenses'

    expense_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 支出ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ユーザーID
    category_id = db.Column(db.Integer, db.ForeignKey('expense_categories.category_id'), nullable=False)  # 支出カテゴリID
    date = db.Column(db.Date, nullable=False)  # 支出日
    amount = db.Column(db.Integer, nullable=False)  # 支出金額
    memo = db.Column(db.Text)  # 備考メモ
    created_at = db.Column(db.DateTime, default=datetime.now)  # 登録日時

    # --- リレーション（オプション） ---
    category = db.relationship('ExpenseCategory', backref='expenses', lazy=True)
    user = db.relationship('User', backref='expenses', lazy=True)

class ExpenseCategory(db.Model):
    __tablename__ = 'expense_categories'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 支出カテゴリID
    name = db.Column(db.String(30), nullable=False)  # カテゴリ名

    # --- リレーション（支出テーブルとの紐づけ） ---
    expenses = db.relationship('Expense', backref='expense_category', lazy=True)