from pydantic import BaseModel
from datetime import date


class HealthSchema(BaseModel):
    user_id: int
    steps: int
    date: date

    class Config:
        orm_mode = True
