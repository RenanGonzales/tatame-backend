# app/schemas/deck.py

from pydantic import BaseModel
from app.schemas.card import CardResponse


class DeckCardAdd(BaseModel):
    card_id: int
    game_id: int
    slot_order: int = 0


class DeckCardUpdate(BaseModel):
    favorited: bool | None = None
    rusty: bool | None = None
    studying: bool | None = None
    slot_order: int | None = None


class DeckCardResponse(BaseModel):
    id: int
    card_id: int
    game_id: int | None
    favorited: bool
    rusty: bool
    studying: bool
    slot_order: int
    card: CardResponse

    class Config:
        from_attributes = True