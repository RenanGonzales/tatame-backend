# app/api/routes/positions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Position
from app.schemas.position import PositionCreate, PositionUpdate, PositionResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/positions", tags=["positions"])


@router.get("/", response_model=list[PositionResponse])
def list_positions(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Position).order_by(Position.display_order).all()


@router.post("/", response_model=PositionResponse, status_code=201)
def create_position(
    data: PositionCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    position = Position(**data.model_dump())
    db.add(position)
    db.commit()
    db.refresh(position)
    return position


@router.put("/{position_id}", response_model=PositionResponse)
def update_position(
    position_id: int,
    data: PositionUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(position, key, value)

    db.commit()
    db.refresh(position)
    return position


@router.delete("/{position_id}", status_code=204)
def delete_position(
    position_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")

    db.delete(position)
    db.commit()