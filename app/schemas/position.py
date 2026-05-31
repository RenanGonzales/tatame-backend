# app/schemas/position.py

from pydantic import BaseModel


class PositionCreate(BaseModel):
    name_en: str
    name_pt: str
    hierarchy_level: int = 0
    display_order: int = 0


class PositionUpdate(BaseModel):
    name_en: str | None = None
    name_pt: str | None = None
    hierarchy_level: int | None = None
    display_order: int | None = None


class PositionResponse(BaseModel):
    id: int
    name_en: str
    name_pt: str
    hierarchy_level: int
    display_order: int

    class Config:
        from_attributes = True