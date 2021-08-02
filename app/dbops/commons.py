"""
Common utilities for database operations
"""
from hashlib import sha256
from sqlalchemy.orm import Session
from app.database.config_db import Base


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
