from pydantic import BaseModel
from enum import Enum


class CardType(str, Enum):
    sweep = "Sweep"
    attack = "Attack"
    recovery = "Recovery"
    control = "Control"
    defense = "Defense"


class CardContext(str, Enum):
    gi = "Gi"
    nogi = "No-Gi"
    mma = "MMA"


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
    name: str
    type: CardType
    context: CardContext = CardContext.gi
    minimum_belt: BeltRank = BeltRank.white
    notes: str | None = None
    illustration_url: str | None = None
    rusty: bool = False
    studying: bool = False


class CardUpdate(BaseModel):
    name: str | None = None
    type: CardType | None = None
    context: CardContext | None = None
    minimum_belt: BeltRank | None = None
    notes: str | None = None
    illustration_url: str | None = None
    rusty: bool | None = None
    studying: bool | None = None


class CardResponse(BaseModel):
    id: int
    position_id: int
    name: str
    type: CardType
    context: CardContext
    minimum_belt: BeltRank
    notes: str | None
    illustration_url: str | None
    rusty: bool
    studying: bool

    class Config:
        from_attributes = True