from app import db
from apps.notification.models import Notification

#登録する関数
def create_notification(user_id, detail):
    notification = Notification(
        user_id=user_id,
        detail=detail
    )
    db.session.add(notification)
    db.session.commit()

    return notification

#更新する関数
def update_notification(notification_id, detail):
    notification = Notification.query.get(notification_id)
    if not notification:
        return None
    notification.detail = detail
    db.session.commit()

    return notification