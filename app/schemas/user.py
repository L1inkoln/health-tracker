from pydantic import BaseModel
from datetime import datetime


class UserSchema(BaseModel):
    telegram_id: int
    start_date: datetime
    target_calories: int = 2000
    target_water: float = 2.0
    target_sleep: int = 8

    class Config:
        orm_mode = True
