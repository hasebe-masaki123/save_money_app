from flask import request,render_template,url_for,Blueprint
from flask_login import current_user
from app import db
from apps.notification.models import Notification


notification = Blueprint(
    "notification",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@notification.route("/notification", methods=["GET", "POST"])
def notifications(): 
    # 現在ユーザーの通知を全件取得
    # notifications = db.session.query(Notification).filter(Notification.user_id == current_user.id).all()
    return render_template("notification.html"
                        #    , notifications=notifications
                           )

