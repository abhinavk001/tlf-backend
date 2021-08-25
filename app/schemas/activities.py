"""
Activity schema
"""
from pydantic import BaseModel
from typing import Optional


class ActivityBase(BaseModel):
    """
    Base Activity model
    """
    name: str
    points: int
    duration: int


class CreateActivity(ActivityBase):
    """
    Create Activity model
    """
    pass


class UpdateActivity(BaseModel):
    """
    Update Activity model
    """
    name: Optional[str] = None
    points: Optional[int] = None
    duration: Optional[int] = None


class ShowActivity(ActivityBase):
    """
    Show activity model
    """
    class Config:
        """
        Enable orm mode
        """
        orm_mode = True


class Activity(ActivityBase):
    """
    Full Activity schema
    """
    id: int
    is_complete: bool 

    class Config:
        """
        Enable ORM mode
        """
        orm_mode = True
