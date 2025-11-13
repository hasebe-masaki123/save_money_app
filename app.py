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

    # データベース設定
    app.config['SQLALCHEMY_DATABASE_URI'] = \
    "mysql+pymysql://{user}:{password}@{host}/{dbName}?charset=utf8".format(
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASS'),
        host = os.getenv('DB_HOST'),
        dbName = os.getenv('DB_NAME')
    )

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Blueprintの登録
    from apps.auth import views as auth_views

    from apps.top import views as top_views
    # from apps.calendar import views as calendar_views
    # from apps.expense import views as expense_views
    # from apps.income import views as income_views
    # from apps.saving import views as saving_views
    # from apps.fixed import views as fixed_views
    # from apps.goal import views as goal_views
    # from apps.graph import views as graph_views
    from apps.notification import views as top_views

    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    
    app.register_blueprint(top_views.top, url_prefix="/top")
    # app.register_blueprint(calendar_views.calendar)
    # app.register_blueprint(expense_views.expense)
    # app.register_blueprint(income_views.income)
    # app.register_blueprint(saving_views.saving)
    # app.register_blueprint(fixed_views.fixed)
    # app.register_blueprint(goal_views.goal)
    # app.register_blueprint(graph_views.graph)

    app.register_blueprint(top_views.notification, url_prefix="/notification")
    



    return app

app = create_app()

if __name__ == "__main__":
    app.run()

