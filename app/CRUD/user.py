from database import models


def get_user_by_email(database, email):
    return database.query(models.User).filter_by(email=email).first()