from pydantic import BaseModel


class SleepSchema(BaseModel):
    user_telegram_id: int
    hours: int

    class Config:
        orm_mode = True
