from datetime import datetime
import random
from .utils import get_days_in_month

EXPENSE_CATEGORIES = ["食費", "交通費", "娯楽", "日用品"]


# ダミーの月別支出データを生成
def generate_monthly_expense_data(month: str):
    year, month_num = map(int, month.split("-"))
    days = get_days_in_month(year, month_num)

    data = {}
    for cat in EXPENSE_CATEGORIES:
        data[cat] = [random.randint(0, 2000) for _ in range(days)]

    return data, days

# 週別に集計
def aggregate_weekly(data_dict, days):
    weekly = {cat: [] for cat in EXPENSE_CATEGORIES}

    for start in range(0, days, 7):
        end = min(start + 7, days)
        for cat in EXPENSE_CATEGORIES:
            weekly[cat].append(sum(data_dict[cat][start:end]))

    return weekly


# 週別データと月合計データを取得
def get_weekly_and_total(month: str):
    monthly_data, days = generate_monthly_expense_data(month)
    weekly = aggregate_weekly(monthly_data, days)

    total = {cat: sum(values) for cat, values in monthly_data.items()}
    week_labels = [f"{1+i*7}~" for i in range(len(next(iter(weekly.values()))))]

    return week_labels, weekly, total
