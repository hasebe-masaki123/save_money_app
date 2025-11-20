
from werkzeug.security import generate_password_hash, check_password_hash
from apps.auth.models import User
from app import db

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None

def is_email_registered(email):
    return User.query.filter_by(email=email).first() is not None


def create_user(email, password):
    hashed = generate_password_hash(password)
    new_user = User(email=email, password_hash=hashed)
    db.session.add(new_user)
    db.session.commit()
    return new_user
