from datetime import datetime, timedelta
from sqlalchemy import extract
from app import db
from apps.expense.models import Expense
from apps.income.models import Income
from apps.saving.models import Saving


def get_days_in_month(year, month):
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    this_month = datetime(year, month, 1)
    return (next_month - this_month).days


# --- 指定テーブルから月データ取得 ---
def get_month_data(model, month: str, user_id=1):
    year, month_num = map(int, month.split("-"))
    rows = (
        model.query
        .filter(model.user_id == user_id)
        .filter(extract("year", model.date) == year)
        .filter(extract("month", model.date) == month_num)
        .all()
    )
    return rows

def get_six_months_data(model, end_month: str, user_id=1):
    end_year, end_month_num = map(int, end_month.split("-"))
    start_month_num = end_month_num - 5
    start_year = end_year
    if start_month_num <= 0:
        start_month_num += 12
        start_year -= 1

    rows = (
        model.query
        .filter(model.user_id == user_id)
        .filter(
            (extract("year", model.date) > start_year) |
            ((extract("year", model.date) == start_year) &
             (extract("month", model.date) >= start_month_num))
        )
        .filter(
            (extract("year", model.date) < end_year) |
            ((extract("year", model.date) == end_year) &
             (extract("month", model.date) <= end_month_num))
        )
        .all()
    )
    return rows


# --- 週別合計を作る ---
def aggregate_weekly_simple(rows, year, month):
    days_in_month = get_days_in_month(year, month)
    weekly = [0] * ((days_in_month + 6) // 7)

    for r in rows:
        week_index = (r.date.day - 1) // 7
        weekly[week_index] += r.amount

    return weekly


# --- mode に応じて切替 ---
def get_weekly_and_total(month: str, mode: str):
    year, month_num = map(int, month.split("-"))

    if mode == "expense":
        rows = get_month_data(Expense, month)
    elif mode == "income":
        rows = get_month_data(Income, month)
    elif mode == "saving":
        rows = get_month_data(Saving, month)

    weekly = aggregate_weekly_simple(rows, year, month_num)
    total = sum(r.amount for r in rows)

    week_labels = [
        f"{1 + 7 * i}~{min(7 * (i + 1), 31)}"
        for i in range(len(weekly))
    ]

    return week_labels, weekly, total

def get_monthly_category_totals(month: str, mode: str, user_id=1):
    year, month_num = map(int, month.split("-"))

    if mode == "expense":
        model = Expense
    elif mode == "income":
        model = Income
    elif mode == "saving":
        model = Saving

    rows = (
        db.session.query(
            model.category,
            db.func.sum(model.amount).label("total_amount")
        )
        .filter(model.user_id == user_id)
        .filter(extract("year", model.date) == year)
        .filter(extract("month", model.date) == month_num)
        .group_by(model.category)
        .all()
    )

    category_totals = {row.category: row.total_amount for row in rows}
    return category_totals

def get_six_months_summary(mode: str, end_month=None, user_id=1):
    """指定月を基準とする過去6か月の月別データを取得"""
    
    if end_month is None:
        # 月が指定されていない場合は現在月を使用
        end_date = datetime.now()
    else:
        year, month = map(int, end_month.split("-"))
        end_date = datetime(year, month, 1)
      
    months = []

    # 月単位で計算
    current_year = end_date.year
    current_month = end_date.month
    
    for i in range(6):
        # i か月前を計算
        target_month = current_month - i
        target_year = current_year
        
        # 月が0以下になった場合は前年に調整
        while target_month <= 0:
            target_month += 12
            target_year -= 1
            
        months.append((target_year, target_month, f"{target_year}-{target_month:02d}"))
    
    months.reverse()  # 古い順にソート
    
    # モデルを選択
    if mode == "expense":
        model = Expense
    elif mode == "income":
        model = Income
    elif mode == "saving":
        model = Saving
    else:
        return [], [], 0
    
    month_labels = []
    monthly_data = []
    total_amount = 0
    
    for year, month, label in months:
        # 各月のデータを集計
        month_total = (
            db.session.query(db.func.sum(model.amount))
            .filter(model.user_id == user_id)
            .filter(extract("year", model.date) == year)
            .filter(extract("month", model.date) == month)
            .scalar() or 0
        )
        
        month_labels.append(f"{month}月")
        monthly_data.append(month_total)
        total_amount += month_total
    
    return month_labels, monthly_data, total_amount

def debug_months_calculation(end_month: str):
    """月計算のデバッグ用関数"""
    year, month = map(int, end_month.split("-"))
    end_date = datetime(year, month, 1)
    
    print(f"基準月: {end_month}")
    
    months = []
    current_year = end_date.year
    current_month = end_date.month
    
    for i in range(6):
        target_month = current_month - i
        target_year = current_year
        
        while target_month <= 0:
            target_month += 12
            target_year -= 1
            
        months.append((target_year, target_month, f"{target_year}-{target_month:02d}"))
        print(f"i={i}: {target_year}年{target_month}月")
    
    months.reverse()
    print("最終結果（古い順）:")
    for year, month, label in months:
        print(f"  {year}年{month}月")
    
    return months
