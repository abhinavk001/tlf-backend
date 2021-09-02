"""
Configure Database
"""
from os import environ
from sqlalchemy import create_engine


def set_up_database(env_variable="DATABASE_URL"):
    """Set up connection to a db"""
    uri = environ.get(env_variable)  # or other relevant config var
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    return create_engine(uri)
