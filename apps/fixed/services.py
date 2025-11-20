from datetime import date
from apps.fixed.models import Fixed, FixedHistory
from app import db


def generate_monthly_fixed(user_id, year, month):
    """指定月の固定費履歴を生成（未生成の場合のみ）"""

    # すでに履歴が存在するか
    exists = FixedHistory.query.filter_by(
        user_id=user_id,
        year=year,
        month=month
    ).first()

    if exists:
        return  # 既にその月の履歴がある場合は処理しない

    # 固定費マスタ一覧
    fixed_items = Fixed.query.filter_by(user_id=user_id).all()

    for item in fixed_items:
        record = FixedHistory(
            user_id=user_id,
            fixed_id=item.fixed_id,
            amount=item.default_amount,
            year=year,
            month=month,
            paid_at=date(year, month, item.billing_day),
            status="pending",
        )
        db.session.add(record)

    db.session.commit()
