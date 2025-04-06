from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from typing import cast

security = HTTPBearer()
SECRET_KEY = cast(str, os.getenv("JWT_SECRET"))


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        if payload.get("bot_id") != os.getenv("BOT_ID"):
            raise HTTPException(status_code=403, detail="Invalid bot ID")
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
