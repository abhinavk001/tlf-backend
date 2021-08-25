"""
Routes for managing user activity
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.activities import CreateActivity, UpdateActivity
from dbops.commons import get_db, commit_changes_to_object, get_current_user_id
from dbops.oauth2 import get_current_user
from database import models


router = APIRouter(
    prefix="/activity",
    tags=["activity"],
)

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_activity(request: CreateActivity, current_user: models.User = Depends(get_current_user), 
                    db: Session = Depends(get_db)):
    """
    Create a new activity
    """
    new_activity = models.Activity(name=request.name, points=request.points, 
                                    duration=request.duration, user_id=get_current_user_id(db, current_user))
    commit_changes_to_object(db, new_activity)
    
    return new_activity


@router.patch("/update/{id}")
def update_activity(id: int, request: UpdateActivity, current_user: models.User = Depends(get_current_user), 
                    db: Session = Depends(get_db)):
    """
    Update an existing activity
    """
    activity = db.query(models.Activity).filter(models.Activity.id == id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    if activity.user_id != get_current_user_id(db, current_user):
        raise HTTPException(status_code=403, detail="You do not have permission to edit this activity")
    
    stored_activity_data = activity.__dict__
    stored_activity_model = UpdateActivity(**stored_activity_data)
    updated_data = request.dict(exclude_unset=True)
    updated_items = stored_activity_model.copy(update=updated_data)

    activity.name = updated_items.name
    activity.points = updated_items.points
    activity.duration = updated_items.duration
    commit_changes_to_object(db, activity)

    return {"data":updated_items}
