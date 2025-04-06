from typing import cast
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import jwt
from datetime import datetime, timedelta

router = APIRouter(tags=["auth"])

# Пароль для получения jwt боту и ключ шифрования
BOT_SECRET = cast(str, os.getenv("BOT_SECRET"))
JWT_SECRET = cast(str, os.getenv("JWT_SECRET"))


class BotAuthRequest(BaseModel):
    password: str


# Выдача токена боту
@router.post("/auth/bot")
def auth_bot(request: BotAuthRequest):
    if request.password != BOT_SECRET:
        raise HTTPException(status_code=403, detail="Invalid password")

    payload = {"sub": "bot", "exp": datetime.utcnow() + timedelta(days=30)}
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return {"access_token": token}
