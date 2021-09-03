"""
Activity schema
"""
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date


class ActivityBase(BaseModel):
    """
    Base Activity model
    """
    name: str
    assign_date: date
    due_date: date
    completed_date: Optional[date] = None


class CreateActivity(ActivityBase):
    """
    Create Activity model
    """
    pass


class CreateActivityByStaff(ActivityBase):
    """
    Assigning an Activity to a Staff member
    """
    email: str


class UpdateActivity(BaseModel):
    """
    Update Activity model
    """
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    assign_date: Optional[date] = None
    due_date: Optional[date] = None
    completed_date: Optional[date] = None
    is_complete: Optional[bool] = None


class ShowActivity(ActivityBase):
    """
    Show activity model
    """
    id: int
    points: int
    is_complete: bool
    class Config:
        """
        Enable orm mode
        """
        orm_mode = True
