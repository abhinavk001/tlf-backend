"""
Routes for managing users.  
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import models
from dbops.oauth2 import get_current_user
from dbops.commons import get_db
from schemas.user import ShowUser
from database import models


router = APIRouter(
    tags=["users"]
)

@router.get("/profile", response_model=ShowUser)
def get_profile(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get the profile of the current user.
    """
    user = db.query(models.User).filter(models.User.email == current_user["sub"]).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    