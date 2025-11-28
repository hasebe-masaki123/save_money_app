from flask import request,render_template,url_for,Blueprint
# from flask_login import current_user
from app import db,os
# import app
# from apps.goal.models import Goal
# from apps.income.models import Income
# from apps.expense.models import Expense
# from apps.saving.models import Saving
# from sqlalchemy import func
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Meiryo'
# from datetime import datetime
from decimal import Decimal, ROUND_DOWN
import time
from matplotlib import rcParams

top = Blueprint(
    "top",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@top.route("/top", methods=["GET", "POST"])
def top_page():
    balance,balance_per, total_income_amount, total_saving_amount,_= week_balance()
    current_amount = SavigGoal(total_income_amount, total_saving_amount)
    return render_template(
        "top.html",
        balance=balance,
        balance_per=balance_per,
        current_amount=current_amount,
    )


#今週の残金を表示
def week_balance():
    #目標金額、現在の達成額、目標期日、収入、支出、貯金をＤＢから取得
    # total_income_amount = db.session.query(func.sum(Income.amount)).filter(Income.user_id == current_user.id).scalar() or 0
    # total_expense_amount = db.session.query(func.sum(Expense.amount)).filter(Expense.user_id == current_user.id).scalar() or 0
    # total_saving_amount = db.session.query(func.sum(Saving.amount)).filter(Saving.user_id == current_user.id).scalar() or 0
    # total_income_amount = db.session.query(func.sum(Income.amount)).filter(Income.user_id == current_user.id).scalar() or 0
    # total_expense_amount = db.session.query(func.sum(Expense.amount)).filter(Expense.user_id == current_user.id).scalar() or 0
    # total_saving_amount = db.session.query(func.sum(Saving.amount)).filter(Saving.user_id == current_user.id).scalar() or 0

    total_income_amount =1000 #収入
    total_expense_amount = 500 #支出
    total_saving_amount = 100 #貯金

    # goal = db.session.query(Goal).filter(Goal.user_id == current_user.id).first()
    # if goal:
    #     target_amount = goal.TARGET_AMOUNT or 0
    #     current_amount = goal.CURRENT_AMOUNT or 0
    #     #今日の日付と期限日を引いて、残りの日数を求める。
    #     deadline_days = (goal.DEADLINE_AT - datetime.today()).days if goal.DEADLINE_AT else 1
    #     deadline_days = max(deadline_days, 1)  # 0除算防止

    target_amount = 2000 #目標額
    current_amount  = 1000 #今の達成額
    deadline_days = 10 #日数

    auto_saving = (target_amount - current_amount) / deadline_days or 0
    auto_saving = Decimal(auto_saving)
    auto_saving = auto_saving.quantize(Decimal('0'), rounding=ROUND_DOWN)

    # else:
    #     auto_saving = 0
    # balance = total_income_amount - total_expense_amount - total_saving_amount - auto_saving
    balance_per = 0

    if auto_saving==0:
        balance = total_income_amount - total_expense_amount - total_saving_amount
    else:
        balance = total_income_amount - total_expense_amount - total_saving_amount - auto_saving

    balance_per=(balance/(total_income_amount-auto_saving))*100 #残金の％表示の計算
    balance_per = Decimal(balance_per) 
    balance_per = balance_per.quantize(Decimal('0'), rounding=ROUND_DOWN) #小数点切り捨て


    return balance,balance_per,total_income_amount,total_saving_amount,auto_saving




#貯金達成度を計算する
def SavigGoal(total_income_amount,total_saving_amount):
    if total_income_amount == 0:
         return 0
    x = (total_saving_amount / total_income_amount) *100
    x = Decimal(x)
    x = x.quantize(Decimal('0.0'), rounding=ROUND_DOWN)
    return x