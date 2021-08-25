"""
Routes for managing users.  
"""
from fastapi import APIRouter, Depends, HTTPException
from database import models
from dbops.oauth2 import get_current_user


router = APIRouter(
    tags=["users"]
)

@router.get("/profile")
def get_profile(current_user: models.User = Depends(get_current_user)):
    """
    Get user data
    """
    pass