from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from pathlib import Path
import os
from flask_wtf import CSRFProtect

# --- 拡張機能の準備 ---
db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    load_dotenv()
    app = Flask(__name__)

    # 秘密鍵
    app.secret_key = os.environ.get("SECRET_KEY")

    # CSRF 保護
    CSRFProtect(app)

    # clickjacking 対策
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    BASE_DIR = Path(__file__).resolve().parent

    # DB 設定
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?charset=utf8"

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # --- Blueprint の読み込み ---
    from apps.auth import views as auth_views
    from apps.top import views as top_views
    from apps.expense import views as expense_views
    from apps.income import views as income_views
    from apps.saving import views as saving_views

    # --- Blueprint の登録 ---
    app.register_blueprint(auth_views.auth_bp) 
    app.register_blueprint(top_views.top_bp)    
    app.register_blueprint(expense_views.expense_bp)
    app.register_blueprint(income_views.income_bp)
    app.register_blueprint(saving_views.saving_bp)

    # --- LoginManager の login_view 設定 ---
    login_manager.login_view = "auth.login"
    login_manager.login_message = ""

    # --- モデルの import ---
    from apps.auth.models import User
    from apps.expense.models import Expense, ExpenseCategory
    from apps.income.models import Income
    from apps.saving.models import Saving

    # --- user_loader 設定 ---
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
