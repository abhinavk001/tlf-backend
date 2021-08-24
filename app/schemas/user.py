"""
User schemas
"""
from typing import Optional
from pydantic import BaseModel
from pydantic.types import constr
from enums.roles import Roles

contact_field = constr(max_length=10, min_length=10, regex="^[0-9]{10}$")


class UserBase(BaseModel):
    """
    Base User Schema
    """
    email: str
    name: str
    contact: contact_field
    points: int
    role: Roles


class CreateUser(UserBase):
    """
    Create User Schema
    """
    password: str


class UserUpdate(BaseModel):
    """
    Update user schema
    """
    email: Optional[str]
    contact: Optional[contact_field]
    name: Optional[str]
    password: Optional[str]


class ShowUser(BaseModel):
    """
    Show basic user data
    """
    name: str
    email: str

    class Config:
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
    activity_id: int

    class Config:
        """Enable ORM mode"""
        orm_mode = True


class Login(BaseModel):
    """
    Login schema
    """
    username: str
    password: str


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
    email: Optional[str] = None