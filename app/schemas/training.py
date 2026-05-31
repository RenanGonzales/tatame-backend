from pydantic import BaseModel
from datetime import date
from app.schemas.card import CardResponse


class TrainingSessionCreate(BaseModel):
    date: date
    duration_min: int | None = None
    result: str | None = None
    notes: str | None = None
    card_ids: list[int] = []


class TrainingSessionUpdate(BaseModel):
    duration_min: int | None = None
    result: str | None = None
    notes: str | None = None


class TrainingCardResponse(BaseModel):
    card: CardResponse

    class Config:
        from_attributes = True


class TrainingSessionResponse(BaseModel):
    id: int
    date: date
    duration_min: int | None
    result: str | None
    notes: str | None
    training_cards: list[TrainingCardResponse] = []

    class Config:
        from_attributes = True