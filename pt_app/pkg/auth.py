from datetime import datetime
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class Authorization:
    """ Авторизация через сервис auth """

    def __init__(self, role: str):
        self.role = role

    def __call__(self,
                 bearer_auth: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
                 ):

        if not bearer_auth:
            raise HTTPException(status_code=401, detail="Not authenticated")
        access, usr = check_token(credentials=bearer_auth, app_role=self.role)
        if not access:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return True, usr


def check_token(credentials: HTTPAuthorizationCredentials, app_role: str) -> tuple:
    """ Check JwtToken auth"""
    try:
        payload = jwt.decode(credentials.credentials, "je3k2d!!dgr1asd", algorithms=["HS256"])
        access = int(datetime.utcnow().timestamp()) < int(payload['exp'])
        if not access:
            return access, None
        roles = [role for role in payload['roles'].split(',')]
        if app_role:
            for role in app_role.split(','):
                if role in roles:
                    return True, payload['usr']
        return False, None
    except jwt.exceptions.InvalidTokenError:
        return False, None
