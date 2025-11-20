from app import db 
from datetime import datetime


#通知テーブル
class Notification(db.Model):
    
    __tablename__ = "notification"

    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    detail = db.Column(db.String(128))
    create_at = db.Column(db.DateTime, default=datetime.now)  