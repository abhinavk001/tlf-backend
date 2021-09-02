import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from schemas.user import TokenData

SECRET_KEY = "f2089a467fcd8eac98baed2ccdc7e1f1d18c4cd99334f032298dda7106b13dc3"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credential_exception):
    """
    Verify JWT token
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = decoded_token.get("sub")
        if email is None:
            raise credential_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credential_exception
    return decoded_token
