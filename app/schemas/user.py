"""
User schemas
"""
from typing import Optional, List
from pydantic import BaseModel, EmailStr, constr
from pydantic.types import constr
from enums.roles import Roles
from schemas.activity import ShowActivity

contact_field = constr(max_length=10, min_length=10, regex="^[0-9]{10}$")


class UserBase(BaseModel):
    """
    Base User Schema
    """
    email: EmailStr
    name: str
    contact: contact_field


class CreateUser(UserBase):
    """
    Create User Schema
    """
    password: constr(min_length=8)


class CreatePrivilagedUser(CreateUser):
    """
    Create Privilaged User Schema
    """
    role: Roles


class CreateAdminUser(CreateUser):
    """
    Create Admin User Schema
    """
    secret_code: str


class UpdateUser(BaseModel):
    """
    Update user schema
    """
    email: Optional[EmailStr] = None
    contact: Optional[contact_field] = None
    name: Optional[str] = None

class UpdateUserByStaff(UpdateUser):
    """
    Updating a user by staff
    """
    points: Optional[int] = None


class ShowUser(BaseModel):
    """
    Show basic user data
    """
    id: int
    name: str
    email: EmailStr
    points: int
    role: Roles
    activities: List[ShowActivity] = []

    class Config():
        """
        Enable ORM mode
        """
        orm_mode = True


class User(UserBase):
    """
    Full User Schema(As in DB)
    """
    id: int
    is_active: bool
    points: int
    role: Roles
    # activity_id: int

    class Config():
        """Enable ORM mode"""
        orm_mode = True


class Login(BaseModel):
    """
    Login schema
    """
    username: EmailStr
    password: constr(min_length=8)


class Token(BaseModel):
    """
    Token schema
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Token data schema
    """
    email: Optional[EmailStr] = None
