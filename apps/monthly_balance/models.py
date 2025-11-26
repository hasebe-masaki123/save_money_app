from app import db

class MonthlyBalance(db.Model):
    __tablename__ = 'monthly_balances'

    balance_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    total_income = db.Column(db.Float, default=0.0)
    total_expense = db.Column(db.Float, default=0.0)
    balance = db.Column(db.Float, default=0.0)

    def __init__(self, user_id, year, month, total_income=0.0, total_expense=0.0):
        self.user_id = user_id
        self.year = year
        self.month = month
        self.total_income = total_income
        self.total_expense = total_expense
        self.balance = total_income - total_expense