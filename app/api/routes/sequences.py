# app/api/routes/sequences.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Sequence, SequenceCard, Game, User
from app.schemas.sequence import SequenceCreate, SequenceUpdate, SequenceResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/games/{game_id}/sequences", tags=["sequences"])


def get_game_or_404(game_id: int, user: User, db: Session) -> Game:
    game = db.query(Game).filter(Game.id == game_id, Game.user_id == user.id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.get("/", response_model=list[SequenceResponse])
def list_sequences(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_game_or_404(game_id, current_user, db)
    return db.query(Sequence).filter(Sequence.game_id == game_id).all()


@router.post("/", response_model=SequenceResponse, status_code=201)
def create_sequence(
    game_id: int,
    data: SequenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_game_or_404(game_id, current_user, db)
    sequence = Sequence(game_id=game_id, name=data.name)
    db.add(sequence)
    db.flush()

    for i, card_data in enumerate(data.cards):
        db.add(SequenceCard(
            sequence_id=sequence.id,
            card_id=card_data.card_id,
            order=card_data.order or i,
        ))

    db.commit()
    db.refresh(sequence)
    return sequence


@router.put("/{sequence_id}", response_model=SequenceResponse)
def update_sequence(
    game_id: int,
    sequence_id: int,
    data: SequenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_game_or_404(game_id, current_user, db)
    sequence = db.query(Sequence).filter(
        Sequence.id == sequence_id,
        Sequence.game_id == game_id
    ).first()
    if not sequence:
        raise HTTPException(status_code=404, detail="Sequence not found")

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(sequence, key, value)

    db.commit()
    db.refresh(sequence)
    return sequence


@router.delete("/{sequence_id}", status_code=204)
def delete_sequence(
    game_id: int,
    sequence_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_game_or_404(game_id, current_user, db)
    sequence = db.query(Sequence).filter(
        Sequence.id == sequence_id,
        Sequence.game_id == game_id
    ).first()
    if not sequence:
        raise HTTPException(status_code=404, detail="Sequence not found")

    db.delete(sequence)
    db.commit()


@router.post("/{sequence_id}/cards", response_model=SequenceResponse)
def add_card_to_sequence(
    game_id: int,
    sequence_id: int,
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_game_or_404(game_id, current_user, db)
    sequence = db.query(Sequence).filter(
        Sequence.id == sequence_id,
        Sequence.game_id == game_id
    ).first()
    if not sequence:
        raise HTTPException(status_code=404, detail="Sequence not found")

    order = len(sequence.cards)
    db.add(SequenceCard(sequence_id=sequence_id, card_id=card_id, order=order))
    db.commit()
    db.refresh(sequence)
    return sequence


@router.delete("/{sequence_id}/cards/{card_id}", response_model=SequenceResponse)
def remove_card_from_sequence(
    game_id: int,
    sequence_id: int,
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_game_or_404(game_id, current_user, db)
    seq_card = db.query(SequenceCard).filter(
        SequenceCard.sequence_id == sequence_id,
        SequenceCard.card_id == card_id
    ).first()
    if not seq_card:
        raise HTTPException(status_code=404, detail="Card not in sequence")

    db.delete(seq_card)
    db.commit()

    sequence = db.query(Sequence).filter(Sequence.id == sequence_id).first()
    db.refresh(sequence)
    return sequence