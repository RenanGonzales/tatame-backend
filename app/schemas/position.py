from pydantic import BaseModel


class PositionCreate(BaseModel):
    name: str
    hierarchy_level: int = 0
    display_order: int = 0


class PositionUpdate(BaseModel):
    name: str | None = None
    hierarchy_level: int | None = None
    display_order: int | None = None


class PositionResponse(BaseModel):
    id: int
    name: str
    hierarchy_level: int
    display_order: int

    class Config:
        from_attributes = True