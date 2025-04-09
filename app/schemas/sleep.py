from pydantic import BaseModel


class SleepSchema(BaseModel):
    user_telegram_id: int
    hours: float

    class Config:
        orm_mode = True
