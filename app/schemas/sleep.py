from pydantic import BaseModel
from datetime import date


class SleepSchema(BaseModel):
    user_id: int
    hours: int
    date: date

    class Config:
        orm_mode = True
