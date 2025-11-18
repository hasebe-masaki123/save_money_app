from datetime import datetime
from sqlalchemy import extract
from app import db
from apps.expense.models import Expense
from apps.income.models import Income
from apps.saving.models import Saving
from apps.fixed.models import FixedCost


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


# --- 週別合計を作る（カテゴリなし） ---
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
