"""
Routes for managing users.  
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import roles
from database import models
from dbops.oauth2 import get_current_user
from dbops.commons import get_db, hash_password, commit_changes_to_object
from schemas.user import ShowUser, CreatePrivilagedUser
from database import models
from dbops.role_dependancy import RoleChecker


router = APIRouter(
    tags=["users"]
)

@router.get("/profile", response_model=ShowUser)
def get_profile(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get the profile of the current user.
    """
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return current_user


allow_create_resource = RoleChecker(["ADMIN"])
@router.get("/p", response_model=ShowUser, dependencies=[Depends(allow_create_resource)])
def get_profile_update(current_user: ShowUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get the profile of the current user.
    """
    return current_user


@router.post("/create", response_model=ShowUser, dependencies=[Depends(allow_create_resource)])
def create_user(request:CreatePrivilagedUser, current_user: ShowUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Create new admins or mods account
    """
    new_user = models.User(name=request.name, email=request.email, 
                            password=hash_password(request.password), contact=request.contact, role=request.role)
    try:
        commit_changes_to_object(db, new_user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User already exists")
    
    return new_user

allow_delete_activity = RoleChecker(["ADMIN", "MODERATOR"])
@router.delete("/delete/{id}", dependencies=[Depends(allow_delete_activity)], status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, current_user: ShowUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Delete an existing activity
    """
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=404, detail="User not found")

    user.delete(synchronize_session=False)

    db.commit()
    return {"message": "User deleted"}

    