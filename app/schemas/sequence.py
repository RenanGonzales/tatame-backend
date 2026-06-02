# app/schemas/sequence.py

from pydantic import BaseModel
from app.schemas.card import CardResponse


class SequenceCardCreate(BaseModel):
    card_id: int
    order: int = 0


class SequenceCreate(BaseModel):
    name: str
    cards: list[SequenceCardCreate] = []


class SequenceUpdate(BaseModel):
    name: str | None = None


class SequenceCardResponse(BaseModel):
    id: int
    card_id: int
    order: int
    card: CardResponse

    class Config:
        from_attributes = True


class SequenceResponse(BaseModel):
    id: int
    game_id: int
    name: str
    cards: list[SequenceCardResponse] = []

    class Config:
        from_attributes = True