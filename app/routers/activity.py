"""
Routes for managing user activity
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
from schemas.activities import CreateActivity, UpdateActivity, CreateActivityByStaff
from dbops.commons import get_db, commit_changes_to_object
from dbops.oauth2 import get_current_user
from database import models
from schemas.user import ShowUser
from dbops.role_dependancy import RoleChecker


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
    new_activity = models.Activity(name=request.name, points=request.points, assign_date=request.assign_date,
                                    due_date=request.due_date, completed_date=request.completed_date,
                                    user_id=current_user.id)
    commit_changes_to_object(db, new_activity)
    
    return new_activity


allow_create_activity = RoleChecker(["ADMIN", "MODERATOR"])
@router.post("/create/staff",dependencies=[Depends(allow_create_activity)], status_code=status.HTTP_201_CREATED)
def create_activity(request: CreateActivityByStaff, current_user: models.User = Depends(get_current_user), 
                    db: Session = Depends(get_db)):
    """
    Assign facilitators an activity by a staff member
    """
    facilitator = db.query(models.User).filter(models.User.email == request.email).first()
    new_activity = models.Activity(name=request.name, points=request.points, assign_date=request.assign_date,
                                    due_date=request.due_date, completed_date=request.completed_date,
                                    user_id=facilitator.id)
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

    if activity.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to edit this activity")
    
    stored_activity_data = activity.__dict__
    stored_activity_model = UpdateActivity(**stored_activity_data)
    updated_data = request.dict(exclude_unset=True)
    updated_items = stored_activity_model.copy(update=updated_data)

    activity.name = updated_items.name
    activity.points = updated_items.points
    activity.assign_date = updated_items.assign_date
    activity.due_date = updated_items.due_date
    activity.completed_date = updated_items.completed_date
    activity.is_complete = updated_items.is_complete
    db.commit()

    return {"detail":updated_items}


allow_delete_activity = RoleChecker(["ADMIN", "MODERATOR"])
@router.delete("/delete/{id}", dependencies=[Depends(allow_delete_activity)], status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, current_user: ShowUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Delete an existing activity
    """
    activity = db.query(models.Activity).filter(models.Activity.id == id)
    if not activity.first():
        raise HTTPException(status_code=404, detail="Activity not found")

    activity.delete(synchronize_session=False)

    db.commit()
    return {"message": "Activity deleted"}
