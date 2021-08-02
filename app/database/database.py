"""
Configure Database
"""
from os import environ
from sqlalchemy import create_engine


def set_up_database(env_variable="DATABASE_URL"):
    """Set up connection to a db"""
    database_url = environ.get(env_variable)
    return create_engine(database_url)
