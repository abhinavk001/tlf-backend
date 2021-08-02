"""
Database Models
"""
import uuid
# For postgres
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.config_db import Base
from app.enums.roles import Roles


class User(Base):
    """
    USER MODEL
    userID, username, name, password(Hashed), is_active, contact, roles(enum), points,
    related to activities
    """
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    username = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=False)
    contact = Column(String(50))
    points = Column(Integer, default=0)
    role = Column(Enum(Roles), default=Roles.USER, nullable=False)
    activities = relationship("Activity", back_populates="user")

    def __init__(self, user_id, username, name, password, contact, roles, points):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.password = password
        self.contact = contact
        self.roles = roles
        self.points = points

    def __repr__(self):
        return '<User %r>' % self.username


class Activity:
    """
    ACTIVITY MODEL
    id, activity name, points, duration, is complete, related to user
    """
    __tablename__ = 'activity'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    name = Column(String(50), nullable=False)
    points = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    is_complete = Column(Boolean, default=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    user = relationship("User", back_populates="activities")

    def __init__(self, activity_id, name, points, duration, is_complete, user_id):
        self.activity_id = activity_id
        self.name = name
        self.points = points
        self.duration = duration
        self.is_complete = is_complete
        self.user_id = user_id

    def __repr__(self):
        return '<Activity %r>' % self.name
