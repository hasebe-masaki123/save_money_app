

from datetime import datetime

# 指定した年月の月の日数を取得
def get_days_in_month(year, month):
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)

    this_month = datetime(year, month, 1)
    return (next_month - this_month).days


# 現在の月を"YYYY-MM"形式で取得
def get_current_month_str():
    return datetime.now().strftime("%Y-%m")
