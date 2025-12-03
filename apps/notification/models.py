from app import db 
from sqlalchemy import func


#通知テーブル
class Notification(db.Model):
    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    detail = db.Column(db.String(128))
    create_at = db.Column(db.DateTime, server_default=func.now())  

