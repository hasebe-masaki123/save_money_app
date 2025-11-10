from flask import Blueprint

top_bp = Blueprint("auth", __name__, url_prefix="/top")

from apps.top import views