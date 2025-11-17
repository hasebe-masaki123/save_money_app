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

#収入テーブル
class Income(db.Model):
    __tablename__ = 'incomes'

    income_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 収入ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ユーザーID
    date = db.Column(db.Date, nullable=False)  # 収入日
    amount = db.Column(db.Integer, nullable=False)  # 収入金額
    memo = db.Column(db.Text)  # 備考メモ
    created_at = db.Column(db.DateTime, default=datetime.now)  # 登録日時

    # --- リレーション（オプション） ---
    user = db.relationship('User', backref='incomes', lazy=True)
    

#貯金テーブル
class Saving(db.Model):
    __tablename__ = 'saving'

    saving_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 貯金ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ユーザーID
    date = db.Column(db.Date, nullable=False)  # 貯金日
    amount = db.Column(db.Integer, nullable=False)  # 金額
    memo = db.Column(db.Text)  # メモ
    created_at = db.Column(db.DateTime, default=datetime.now)  # 登録日時

    # --- リレーション（ユーザーと紐づけ） ---
    user = db.relationship('User', backref='savings', lazy=True)


