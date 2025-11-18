# apps/graphs/services.py
# =======================

from datetime import datetime

# ① DemoRow（デモ用モデル）
class DemoRow:
    def __init__(self, date, amount):
        self.date = date
        self.amount = amount


# ② デモ用の固定データ
DEMO_DATA = {
    "expense": [
        DemoRow(datetime(2025, 1, 2), 1200),
        DemoRow(datetime(2025, 1, 5), 2400),
        DemoRow(datetime(2025, 1, 12), 900),
        DemoRow(datetime(2025, 1, 20), 3100),
        DemoRow(datetime(2025, 1, 28), 1500),
    ],
    "income": [
        DemoRow(datetime(2025, 1, 1), 20000),
        DemoRow(datetime(2025, 1, 15), 18000),
    ],
    "saving": [
        DemoRow(datetime(2025, 1, 10), 5000),
        DemoRow(datetime(2025, 1, 25), 6000),
    ]
}


# ③ 本来DBを使う get_month_data（デモ版）
def get_month_data(model, month: str, user_id=1):
    # 今回は DB なしなのでダミー
    return ["dummy1", "dummy2"]


# ④ 週集計
def aggregate_weekly_simple(rows, year, month):
    weeks = [0, 0, 0, 0, 0]  # 5週分

    for r in rows:
        week_index = (r.date.day - 1) // 7
        weeks[week_index] += r.amount

    return weeks


# ⑤ mode に応じて切替（デモデータ使用）
def get_weekly_and_total(month: str, mode: str):
    year, month_num = map(int, month.split("-"))

    # Demo の固定データを取得
    rows = DEMO_DATA.get(mode, [])

    weekly = aggregate_weekly_simple(rows, year, month_num)
    total = sum(r.amount for r in rows)

    week_labels = [
        f"{1 + 7 * i}~{min(7 * (i + 1), 31)}"
        for i in range(len(weekly))
    ]

    return week_labels, weekly, total
