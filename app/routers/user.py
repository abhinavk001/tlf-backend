"""
Routes for managing users.  
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import models
from dbops.oauth2 import get_current_user
from dbops.commons import get_db, hash_password, commit_changes_to_object, remove_time
from schemas.user import ShowUser, CreatePrivilagedUser, UpdateUser, UpdateUserByStaff
from database import models
from dbops.role_dependancy import RoleChecker
from CRUD.user import save_updated_user, save_updated_user_by_staff, get_user_by_id, delete_user, save_deactivated_user


router = APIRouter(
    tags=["users"]
)

@router.get("/profile", response_model=ShowUser)
def get_profile(current_user: models.User=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get the profile of the current user.
    """
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
  
    user_info = db.query(models.User).filter(models.User.email == current_user.email).first()
    return user_info


allow_view_others_progress = RoleChecker(["ADMIN", "MODERATOR"])
@router.get("/profile/staff" ,dependencies=[Depends(allow_view_others_progress)])
def get_progess(current_user: ShowUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get the progress of all facilitators.
    """
    all_activity = db.query(
                            models.Activity, models.User.name, models.User.id, models.User.stack, models.User.email).order_by(
                            models.Activity.assign_date.desc()).filter(
                            models.Activity.user.has(is_active=True)).filter(
                            models.Activity.user_id == models.User.id).all()
    all_activity = list(map(remove_time, all_activity))
    return all_activity


@router.patch("/update/{id}")
def update_user(id: int, request: UpdateUser, current_user: models.User = Depends(get_current_user), 
                    db: Session = Depends(get_db)):
    """
    Update an existing User
    """
    user = get_user_by_id(id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to edit this User")

    save_updated_user(db, user, request)
    return {
        "detail": "User updated successfully"
    }


allow_modify_other_users = RoleChecker(["ADMIN", "MODERATOR"])
@router.patch("/update/staff/{id}", dependencies=[Depends(allow_modify_other_users)])
def update_user_by_staff(id: int, request: UpdateUserByStaff,
                        current_user: models.User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    """
    Update an existing User by a staff member.
    """
    user = get_user_by_id(id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    save_updated_user_by_staff(db, user, request)
    return {
        "detail": "User updated successfully"
    }


allow_create_user = RoleChecker(["ADMIN"])
@router.post("/create", response_model=ShowUser, dependencies=[Depends(allow_create_user)])
def create_user(request:CreatePrivilagedUser, current_user: ShowUser = Depends(get_current_user),
                db: Session = Depends(get_db)):
    """
    Create new admins or mods account
    """
    new_user = models.User(name=request.name, email=request.email, 
                            password=hash_password(request.password), contact=request.contact,
                            role=request.role)
    try:
        commit_changes_to_object(db, new_user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User already exists")

    return new_user


@router.patch("/deactivate-user/{id}", dependencies=[Depends(allow_modify_other_users)])
def deactivate_user(id: int, current_user: models.User = Depends(get_current_user), 
                    db: Session = Depends(get_db)):
    """
    Update an existing User by a staff member.
    """
    user = get_user_by_id(id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    save_deactivated_user(db, user)
    return {
        "detail": "User deactivated successfully"
    }


allow_delete_activity = RoleChecker(["ADMIN", "MODERATOR"])
@router.delete("/delete/{id}", dependencies=[Depends(allow_delete_activity)],
                status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, current_user: ShowUser = Depends(get_current_user),
            db: Session = Depends(get_db)):
    """
    Delete an existing User
    """
    delete_user(db, id, current_user)
    return {"detail": "User deleted"}
