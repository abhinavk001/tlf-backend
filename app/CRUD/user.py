"""
CRUD operations for User
"""
from fastapi import HTTPException
from database import models
from schemas.user import UpdateUser
from enums.roles import hierarchy


def get_user_by_id(id, db):
    """
    Return a user object by id
    """
    return db.query(models.User).filter_by(id=id).first()


def get_user_by_email(database, email):
    """
    Return a user object by email
    """
    return database.query(models.User).filter_by(email=email).first()


def parse_user_request(user, request):
    """
    Parse request data
    """
    stored_user_data = user.__dict__
    stored_user_model = UpdateUser(**stored_user_data)
    updated_data = request.dict(exclude_unset=True)
    updated_items = stored_user_model.copy(update=updated_data)
    return updated_items


def save_updated_user(db, user, request):
    """
    Save updated user
    """
    updated_items = parse_user_request(user, request)
    user.name = updated_items.name
    user.email = updated_items.email
    user.contact = updated_items.contact
    user.stack = updated_items.stack
    db.commit()


def save_updated_user_by_staff(db, user, request):
    """
    Save updated user
    """
    updated_items = parse_user_request(user, request)
    user.name = updated_items.name
    user.email = updated_items.email
    user.contact = updated_items.contact
    user.points = updated_items.points
    user.stack = updated_items.stack
    db.commit()


def save_deactivated_user(db, user):
    """
    Deactivate a user
    """
    user.is_active = False
    db.commit()


def delete_user(db, id, current_user):
    """
    Delete a user
    """
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=404, detail="User not found")

    if hierarchy[current_user.role] <= hierarchy[user.first().role]:
        raise HTTPException(status_code=403, detail="You don't have permission to delete that user")
    
    db.query(models.Activity).filter(models.Activity.user_id == id).delete(synchronize_session=False)

    user.delete(synchronize_session=False)

    db.commit()
