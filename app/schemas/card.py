# app/schemas/card.py

from pydantic import BaseModel
from enum import Enum


class CardType(str, Enum):
    takedown = "takedown"
    guard_pass = "guard_pass"
    sweep = "sweep"
    attack = "attack"
    recovery = "recovery"
    control = "control"
    defense = "defense"

class CardPerspective(str, Enum):
    top = "top"
    bottom = "bottom"
    neutral = "neutral"


class CardContext(str, Enum):
    gi = "gi"
    nogi = "nogi"
    mma = "mma"


class BeltRank(str, Enum):
    white = "white"
    gray = "gray"
    yellow = "yellow"
    orange = "orange"
    green = "green"
    blue = "blue"
    purple = "purple"
    brown = "brown"
    black = "black"


class CardCreate(BaseModel):
    name_en: str
    name_pt: str
    type: CardType
    context: CardContext = CardContext.gi
    minimum_belt: BeltRank = BeltRank.white
    notes_en: str | None = None
    notes_pt: str | None = None
    illustration_url: str | None = None
    perspective: CardPerspective = CardPerspective.neutral


class CardUpdate(BaseModel):
    name_en: str | None = None
    name_pt: str | None = None
    type: CardType | None = None
    context: CardContext | None = None
    minimum_belt: BeltRank | None = None
    notes_en: str | None = None
    notes_pt: str | None = None
    illustration_url: str | None = None
    perspective: CardPerspective | None = None


class CardResponse(BaseModel):
    id: int
    position_id: int
    name_en: str
    name_pt: str
    type: CardType
    context: CardContext
    minimum_belt: BeltRank
    notes_en: str | None
    notes_pt: str | None
    illustration_url: str | None
    perspective: CardPerspective | None = None

    class Config:
        from_attributes = True