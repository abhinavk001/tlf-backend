"""
CRUD operation on activities
"""
from fastapi import HTTPException
from schemas.activity import UpdateActivity
from database import models


def get_activity_by_id(id, db):
    """
    Query for a specific activity by id
    """
    activity = db.query(models.Activity).filter(models.Activity.id == id).first()
    return activity


def parse_activity_request(activity, request):
    """
    Parse request data
    """
    stored_activity_data = activity.__dict__
    stored_activity_model = UpdateActivity(**stored_activity_data)
    updated_data = request.dict(exclude_unset=True)
    updated_items = stored_activity_model.copy(update=updated_data)
    return updated_items


def assign_points_on_completion(current_activity, request, db):
    """
    Assign points to the user based on activity completion
    """
    if current_activity.is_marked == False:
        if current_activity.is_complete == False and  request.is_complete == True:
            current_user = db.query(models.User).filter(models.User.id == current_activity.user_id).first()
            current_user.points += current_activity.points
            db.commit()


def save_updated_activity(activity, db, request):
    """
    Save modified activity details to database
    """
    updated_items = parse_activity_request(activity, request)

    assign_points_on_completion(activity, updated_items, db)

    activity.name = updated_items.name
    activity.points = updated_items.points
    activity.assign_date = updated_items.assign_date
    activity.due_date = updated_items.due_date
    activity.completed_date = updated_items.completed_date
    activity.is_complete = updated_items.is_complete
    db.commit()


def delete_activity(id, db):
    """
    Delete activity from database
    """
    activity = db.query(models.Activity).filter(models.Activity.id == id)
    if not activity.first():
        raise HTTPException(status_code=404, detail="Activity not found")

    activity.delete(synchronize_session=False)

    db.commit()