"""
Routes for managing user activity
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
from schemas.activity import CreateActivity, UpdateActivity, CreateActivityByStaff
from dbops.commons import get_db, commit_changes_to_object
from dbops.oauth2 import get_current_user
from database import models
from schemas.user import ShowUser
from dbops.role_dependancy import RoleChecker
from CRUD.activity import save_updated_activity, get_activity_by_id, delete_activity


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
def assign_activity(request: CreateActivityByStaff, current_user: models.User = Depends(get_current_user), 
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
    activity = get_activity_by_id(id, db)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    if activity.user_id == current_user.id:
        save_updated_activity(activity, db, request)
    elif activity.user != current_user.id and current_user.role.value != "USER":
        save_updated_activity(activity, db, request)
    else:
        raise HTTPException(status_code=403, detail="You do not have permission to edit this activity")

    return {"detail":"Successfully updated activity"}


allow_delete_activity = RoleChecker(["ADMIN", "MODERATOR"])
@router.delete("/delete/{id}", dependencies=[Depends(allow_delete_activity)], status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, current_user: ShowUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Delete an existing activity
    """
    delete_activity(id, db)
    return {"message": "Activity deleted"}
