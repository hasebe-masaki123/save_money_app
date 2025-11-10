
from app import db



#ユーザーテーブル
class User(db.Models):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30),nullable=False)
    password = db.Column(db.String(128),nullable=False)
    create_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)


#ロジック書く

