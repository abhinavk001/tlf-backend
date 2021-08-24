"""
Database Models
"""
from sqlalchemy import Column, String, Boolean, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database.config_db import Base
from enums.roles import Roles


class Activity(Base):
    """
    ACTIVITY MODEL
    id, activity name, points, duration, is complete, related to user
    """
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    points = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    is_complete = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="activities")

    def __repr__(self):
        return '<Activity %r>' % self.name


class User(Base):
    """
    USER MODEL
    userID, email, name, password(Hashed), is_active, contact, roles(enum), points,
    related to activities
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50),unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=False)
    contact = Column(String(50))
    points = Column(Integer, default=0)
    role = Column(Enum(Roles), default=Roles.USER, nullable=False)
    activities = relationship("Activity", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.name
