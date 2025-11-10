from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from pathlib import Path

from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 
import os
from flask_wtf import CSRFProtect


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()



def create_app():
    app = Flask(__name__)

    #CSRFトークンのために必要な秘密鍵
    app.secret_key = os.environ.get("SECRET_KEY")
    #csrf保護を有効化
    CSRFProtect(app)

    BASE_DIR = Path(__file__).resolve().parent

    #全ページにclickjacking対策を適応させるコード
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    # MySQLの場合の設定例
    # app.config.update(
    #     SECRET_KEY="dev-secret-key",
    #     SQLALCHEMY_DATABASE_URI=f"sqlite:///{BASE_DIR / 'app.db'}",
    #     SQLALCHEMY_TRACK_MODIFICATIONS=False,
    # )

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from apps.auth import auth_bp
    from apps.top import top_bp
    from apps.calendar import calendar_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(transaction_bp)

    return app

