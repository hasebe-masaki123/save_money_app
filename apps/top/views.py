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
    balance, total_income_amount, total_saving_amount, auto_saving = week_balance()
    current_amount = SavigGoal(total_income_amount, total_saving_amount)
    graph_dir = os.path.join(top.static_folder, "IMG")
    os.makedirs(graph_dir, exist_ok=True)
    graph_path = os.path.join(graph_dir,"graph.png") 
    PieChart(balance, graph_path)
    graph_filename = url_for('top.static', filename='IMG/graph.png', v=time.time())
    return render_template(
        "top.html",
        balance=balance,
        current_amount=current_amount,
        filename=graph_filename
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

    total_income_amount =100000
    total_expense_amount = 50000
    total_saving_amount = 10000

    # goal = db.session.query(Goal).filter(Goal.user_id == current_user.id).first()
    # if goal:
    #     target_amount = goal.TARGET_AMOUNT or 0
    #     current_amount = goal.CURRENT_AMOUNT or 0
    #     #今日の日付と期限日を引いて、残りの日数を求める。
    #     deadline_days = (goal.DEADLINE_AT - datetime.today()).days if goal.DEADLINE_AT else 1
    #     deadline_days = max(deadline_days, 1)  # 0除算防止
    total_income_amount =100000
    total_expense_amount = 50000
    total_saving_amount = 10000

    # goal = db.session.query(Goal).filter(Goal.user_id == current_user.id).first()
    # if goal:
    #     target_amount = goal.TARGET_AMOUNT or 0
    #     current_amount = goal.CURRENT_AMOUNT or 0
    #     #今日の日付と期限日を引いて、残りの日数を求める。
    #     deadline_days = (goal.DEADLINE_AT - datetime.today()).days if goal.DEADLINE_AT else 1
    #     deadline_days = max(deadline_days, 1)  # 0除算防止

    target_amount = 200000
    current_amount  = 100000
    deadline_days = 60

    auto_saving = (target_amount - current_amount) / deadline_days or 0
    auto_saving = Decimal(auto_saving)
    auto_saving = auto_saving.quantize(Decimal('0'), rounding=ROUND_DOWN)
    # else:
    #     auto_saving = 0
    # balance = total_income_amount - total_expense_amount - total_saving_amount - auto_saving
    if auto_saving==0:
        balance = total_income_amount - total_expense_amount - total_saving_amount
    else:
        balance = total_income_amount - total_expense_amount - total_saving_amount - auto_saving
        balance = total_income_amount - total_expense_amount - total_saving_amount - auto_saving

    return balance,total_income_amount,total_saving_amount,auto_saving



#残金のグラフを作成する
def PieChart(balance, save_path):  
    #グラフの縦横の比率と背景の色
    plt.figure(figsize=(4, 4))

    rcParams['font.family'] = 'Meiryo'

    # 例: 目標額と現在残金

    month_expense_amount = 20000 # 支出
    balance = balance     # 残金

    # 円グラフ用のサイズ計算
    if balance >= month_expense_amount:
        sizes = [month_expense_amount, balance - month_expense_amount]
        labels = ["支出", "残金"]
    else:
        sizes = [balance, month_expense_amount - balance]  # 残金と不足分
        labels = ["残金", "不足分"]
        labels = ["残金", "支出"]

    # スライスの色を指定
    colors = ['#A4C6FF', "#BAD3FF"] 

    #0の値を持つスライスを円グラフから取り除く
    sizes, labels, colors = zip(*[(s, l, c) for s, l, c in zip(sizes, labels, colors) if s > 0])

    #グラフの色とか見た目
    wedges,texts, autotexts = plt.pie(
        sizes, 
        labels=labels, 
        autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '',
        startangle=90, 
        counterclock=False,
        colors=colors,          
        wedgeprops={'edgecolor': "#5171A9FF"},
        labeldistance=1.2,      # ラベルの位置
    )

    # 色指定
    plt.setp(texts, color="dimgray", fontsize=25)      # ラベル
    plt.setp(autotexts, color="#fff", fontsize=22) # %のとこ

    # グラフを保存する
    plt.savefig(save_path, bbox_inches='tight', facecolor='#fff')
    plt.close()



#貯金達成度を計算する
def SavigGoal(total_income_amount,total_saving_amount):
    if total_income_amount == 0:
         return 0
    x = (total_saving_amount / total_income_amount) *100
    x = Decimal(x)
    x = x.quantize(Decimal('0.0'), rounding=ROUND_DOWN)
    return x