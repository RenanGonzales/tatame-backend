# app/api/routes/deck.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Deck, Card, User
from app.schemas.deck import DeckCardAdd, DeckCardUpdate, DeckCardResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/deck", tags=["deck"])


@router.get("/", response_model=list[DeckCardResponse])
def list_deck(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Deck).filter(Deck.user_id == current_user.id).all()


@router.get("/{game_id}", response_model=list[DeckCardResponse])
def list_deck_by_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Deck).filter(
        Deck.user_id == current_user.id,
        Deck.game_id == game_id
    ).all()


@router.post("/", response_model=DeckCardResponse, status_code=201)
def add_to_deck(
    data: DeckCardAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    card = db.query(Card).filter(Card.id == data.card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    existing = db.query(Deck).filter(
        Deck.user_id == current_user.id,
        Deck.card_id == data.card_id,
        Deck.game_id == data.game_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Card already in deck")

    entry = Deck(user_id=current_user.id, **data.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.patch("/{deck_id}", response_model=DeckCardResponse)
def update_deck_card(
    deck_id: int,
    data: DeckCardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entry = db.query(Deck).filter(
        Deck.id == deck_id,
        Deck.user_id == current_user.id
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Deck entry not found")

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(entry, key, value)

    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{deck_id}", status_code=204)
def remove_from_deck(
    deck_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entry = db.query(Deck).filter(
        Deck.id == deck_id,
        Deck.user_id == current_user.id
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Deck entry not found")

    db.delete(entry)
    db.commit()