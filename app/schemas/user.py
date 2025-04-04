from pydantic import BaseModel
from datetime import datetime


class UserSchema(BaseModel):
    telegram_id: int
    start_date: datetime

    class Config:
        orm_mode = True
