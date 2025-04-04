from pydantic import BaseModel


class HealthSchema(BaseModel):
    user_telegram_id: int
    steps: int

    class Config:
        orm_mode = True
