"""
User schemas
"""
from typing import Optional
from pydantic import BaseModel
from pydantic.types import constr
from app.enums.roles import Roles

contact_field = constr(max_length=10, min_length=10, regex="^[0-9]{10}$")


class UserBase(BaseModel):
    """
    Base User Schema
    """
    username: str
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
    username: Optional[str]
    contact: Optional[contact_field]
    name: Optional[str]
    password: Optional[str]


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
