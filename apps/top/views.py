from flask import request,render_template,url_for,Blueprint
from flask_login import current_user
from app import db,os
import app
from apps.goal.models import Goals
from apps.income.models import Income
from apps.expense.models import Expense
from apps.saving.models import Saving
from sqlalchemy import func
import matplotlib.pyplot as plt
from datetime import datetime

top = Blueprint(
    "top",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@top.route("/top", methods=["GET", "POST"])
def top():
    balance,total_income_amount,total_saving_amount,auto_saving = week_balance()

    return render_template("top/top.html",balance=balance)

#今週の残金を表示
def week_balance():
    #目標金額、現在の達成額、目標期日、収入、支出、貯金をＤＢから取得
    total_income_amount = db.session.query(func.sum(Income.amount)).filter(Income.user_id == current_user.id).scalar() or 0
    total_expense_amount = db.session.query(func.sum(Expense.amount)).filter(Expense.user_id == current_user.id).scalar() or 0
    total_saving_amount = db.session.query(func.sum(Saving.amount)).filter(Saving.user_id == current_user.id).scalar() or 0

    goal = db.session.query(Goals).filter(Goals.user_id == current_user.id).first()
    if goal:
        target_amount = goal.TARGET_AMOUNT or 0
        current_amount = goal.CURRENT_AMOUNT or 0
        #今日の日付と期限日を引いて、残りの日数を求める。
        deadline_days = (goal.DEADLINE_AT - datetime.today()).days if goal.DEADLINE_AT else 1
        deadline_days = max(deadline_days, 1)  # 0除算防止

        auto_saving = (target_amount - current_amount) / deadline_days
    else:
        auto_saving = 0
    balance = total_income_amount - total_expense_amount - total_saving_amount - auto_saving

    return balance,total_income_amount,total_saving_amount,auto_saving



#残金のグラフを作成する
def PieChart(balance):  
    x = [max(balance, 0), max(-balance, 0)]

    labels = ["残金", "不足分"]

    plt.pie(x, labels=labels, autopct="%1.1f%%", startangle=90, counterclock=False)
    plt.title("今週の残金グラフ")

    # グラフを保存する
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], "graph.png")
    plt.savefig(save_path)
    plt.close()

#グラフ表示
def Display_IMG():
    graph = url_for('static', filename='IMG/graph.png')
    return render_template("top.html", filename=graph)






#貯金達成度を計算する
def SavigGoal(total_income_amount,total_saving_amount):
    if total_income_amount == 0:
         return 0
    return (total_saving_amount / total_income_amount) *100