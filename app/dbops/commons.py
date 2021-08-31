"""
Common utilities for database operations
"""
from hashlib import sha256
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database.config_db import Base, SessionLocal


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt
    """
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)


def verify(hashed_password: str, plain_password: str):
    """
    Verify a password is same as hashed password
    """
    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(plain_password, hashed_password)


def hash_string(*kwargs):
    """
    Hash string with sha256
    """
    return sha256(("".join([str(i) for i in kwargs])).encode("utf-8")).hexdigest()


def commit_changes_to_object(database: Session, obj: Base):
    """Finish the database transaction and refresh session"""
    database.add(obj)
    database.commit()
    database.refresh(obj)


def get_db():
    """
    Get database session
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
    

# def send_reset_email(user):
#     token = user.get_reset_token()
#     msg = Message('Password reset request', sender='noreply@demo.com', recipients=[user.email])
#     msg.body = f'''To reset your password, visit the following link:
#     { url_for('users.reset_token', token=token, _external=True) }
#     If you did not make this request then please ingnore this mail.
#     '''
#     mail.send(msg)
