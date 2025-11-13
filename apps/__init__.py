# apps/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
    db.init_app(app)
    migrate.init_app(app, db)

    from apps.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app