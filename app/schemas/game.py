# app/schemas/game.py

from pydantic import BaseModel
from datetime import datetime


class GameCreate(BaseModel):
    name: str


class GameUpdate(BaseModel):
    name: str | None = None


class GameResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True