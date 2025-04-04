from pydantic import BaseModel


class NutritionSchema(BaseModel):
    user_telegram_id: int
    calories: int
    water: int

    class Config:
        orm_mode = True
