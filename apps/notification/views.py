from flask import request, render_template, url_for, redirect, Blueprint
from flask_login import current_user, login_required
from apps.notification.services import create_notification
from apps.notification.models import Notification


notification = Blueprint(
    "notification",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@notification.route("/notification", methods=["GET", "POST"])
@login_required
def notifications(): 
    if request.method == "POST":
        detail = request.form.get("detail")
        create_notification(current_user.user_id, detail) 
        return redirect(url_for("notification.notifications")) 

    notifications = (
        Notification.query
        .filter(Notification.user_id == current_user.user_id)
        .order_by(Notification.create_at.desc())
        .all()
    )

    return render_template(
        "notification.html",
        notifications=notifications
    )



