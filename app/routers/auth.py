"""
Routes related to user authentication
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.user import Login, CreateUser, ShowUser
from dbops.commons import get_db, verify, commit_changes_to_object, hash_password
from dbops.tokens import create_access_token
from dbops.oauth2 import get_current_user
from database import models


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

@router.post("/login")
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    User login
    """
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Email")
    
    if not verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")

    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", response_model=ShowUser)
def signup(request:CreateUser, db: Session = Depends(get_db)):
    """
    Create a new user
    """
    new_user = models.User(name=request.name, email=request.email, password=hash_password(request.password))
    try:
        commit_changes_to_object(db, new_user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User already exists")
    
    return new_user


@router.get("/profile")
def profile(gcurrent_user: models.User = Depends(get_current_user)):
    return {"message": "Hello World"}
