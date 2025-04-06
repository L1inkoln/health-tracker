from pydantic import BaseModel


class NutritionSchema(BaseModel):
    user_telegram_id: int
    calories: int
    water: float

    class Config:
        orm_mode = True
