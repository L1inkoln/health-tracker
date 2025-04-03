from pydantic import BaseModel
from datetime import date


class NutritionSchema(BaseModel):
    user_id: int
    calories: int
    water: float
    date: date

    class Config:
        orm_mode = True
