"""
Roles Enum
"""
from enum import Enum


class Roles(Enum):
    """
    The role enum
    """
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    USER = "USER"


hierarchy = {
    Roles.ADMIN: 2,
    Roles.MODERATOR: 1,
    Roles.USER: 0
}
