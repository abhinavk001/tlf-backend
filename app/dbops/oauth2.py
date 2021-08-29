from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from dbops.commons import get_db
from .tokens import SECRET_KEY, ALGORITHM
from schemas.user import TokenData, User
from CRUD.user import get_user_by_email


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError as jwt_exception:
        raise credentials_exception from jwt_exception
    user = get_user_by_email(database=db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return User(**user.__dict__)