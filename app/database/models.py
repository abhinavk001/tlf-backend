"""
Database Models
"""
from sqlalchemy import Column, String, Boolean, Integer, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from database.config_db import Base
from enums.roles import Roles, Stacks
from dbops.tokens import SECRET_KEY


class Activity(Base):
    """
    ACTIVITY MODEL
    id, activity name, points, duration, is complete, related to user
    """
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    points = Column(Integer, nullable=False)
    assign_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    completed_date = Column(DateTime)
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
    is_active = Column(Boolean, default=True)
    contact = Column(String(50))
    points = Column(Integer, default=0)
    stack = Column(Enum(Stacks))
    role = Column(Enum(Roles), default=Roles.USER, nullable=False)
    activities = relationship("Activity", back_populates="user")

    def get_reset_token(self, expires_sec=1800):
        """
        Create and return token for reset password functionality
        """
        token = Serializer(SECRET_KEY, expires_sec)
        return token.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """
        Verify the reset password token passed
        """
        token = Serializer(SECRET_KEY)
        try:
            user_id = token.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return '<User %r>' % self.name
