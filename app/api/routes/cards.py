from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Card, Position, User
from app.schemas.card import CardCreate, CardUpdate, CardResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/positions/{position_id}/cards", tags=["cards"])


def get_position_or_404(position_id: int, user: User, db: Session) -> Position:
    position = db.query(Position).filter(
        Position.id == position_id,
        Position.user_id == user.id
    ).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position


@router.get("/", response_model=list[CardResponse])
def list_cards(
    position_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_position_or_404(position_id, current_user, db)
    return db.query(Card).filter(Card.position_id == position_id).all()


@router.post("/", response_model=CardResponse, status_code=201)
def create_card(
    position_id: int,
    data: CardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_position_or_404(position_id, current_user, db)
    card = Card(**data.model_dump(), position_id=position_id)
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


@router.put("/{card_id}", response_model=CardResponse)
def update_card(
    position_id: int,
    card_id: int,
    data: CardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_position_or_404(position_id, current_user, db)
    card = db.query(Card).filter(
        Card.id == card_id,
        Card.position_id == position_id
    ).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(card, key, value)

    db.commit()
    db.refresh(card)
    return card


@router.delete("/{card_id}", status_code=204)
def delete_card(
    position_id: int,
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_position_or_404(position_id, current_user, db)
    card = db.query(Card).filter(
        Card.id == card_id,
        Card.position_id == position_id
    ).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    db.delete(card)
    db.commit()