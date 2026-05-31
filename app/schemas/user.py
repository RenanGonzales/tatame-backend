from pydantic import BaseModel, EmailStr
from enum import Enum


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


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    belt: BeltRank = BeltRank.white
    stripes: int = 0


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    belt: BeltRank
    stripes: int

    class Config:
        from_attributes = True