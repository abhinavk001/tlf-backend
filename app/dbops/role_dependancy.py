from typing import List
from fastapi import HTTPException
from fastapi import Depends
from database.models import User
from dbops.oauth2 import get_current_user


class RoleChecker:
    """
    Class for checking if the current user has the required role.
    """
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        role=user.role

        if role.value not in self.allowed_roles:
            raise HTTPException(status_code=403, detail=f"""Operation not permitted.
                                                            Your role: {role.value}. 
                                                            Required role: {self.allowed_roles}""")
