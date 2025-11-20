from app import db
from datetime import datetime
from apps.auth.models import User




# ==========================
# 支出カテゴリテーブル
# ==========================
class ExpenseCategory(db.Model):
    __tablename__ = 'expense_categories'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 支出カテゴリID
    name = db.Column(db.String(30), nullable=False)  # カテゴリ名

    # --- リレーション（支出テーブルへ） ---
    expenses = db.relationship('Expense', backref='expense_category', lazy=True)

    def __repr__(self):
        return f"<ExpenseCategory {self.name}>"


# ==========================
# 支出テーブル
# ==========================
class Expense(db.Model):
    __tablename__ = 'expenses'

    expense_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 支出ID

    # ---- 外部キー（修正ポイント） ----
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id'),  # ← 外部キー修正済
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('expense_categories.category_id'),
        nullable=False
    )

    date = db.Column(db.Date, nullable=False)  # 支出日
    amount = db.Column(db.Integer, nullable=False)  # 支出金額
    memo = db.Column(db.Text)  # 備考メモ
    created_at = db.Column(db.DateTime, default=datetime.now)  # 登録日時

    def __repr__(self):
        return f"<Expense {self.amount}円>"
