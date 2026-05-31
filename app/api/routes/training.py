from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import TrainingSession, TrainingCard, Card, User
from app.schemas.training import TrainingSessionCreate, TrainingSessionUpdate, TrainingSessionResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/training", tags=["training"])


@router.get("/", response_model=list[TrainingSessionResponse])
def list_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(TrainingSession).filter(TrainingSession.user_id == current_user.id).order_by(TrainingSession.date.desc()).all()


@router.post("/", response_model=TrainingSessionResponse, status_code=201)
def create_session(
    data: TrainingSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = TrainingSession(
        user_id=current_user.id,
        date=data.date,
        duration_min=data.duration_min,
        result=data.result,
        notes=data.notes,
    )
    db.add(session)
    db.flush()

    for card_id in data.card_ids:
        card = db.query(Card).filter(Card.id == card_id).first()
        if not card:
            raise HTTPException(status_code=404, detail=f"Card {card_id} not found")
        db.add(TrainingCard(training_session_id=session.id, card_id=card_id))

    db.commit()
    db.refresh(session)
    return session


@router.get("/{session_id}", response_model=TrainingSessionResponse)
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(TrainingSession).filter(
        TrainingSession.id == session_id,
        TrainingSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.patch("/{session_id}", response_model=TrainingSessionResponse)
def update_session(
    session_id: int,
    data: TrainingSessionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(TrainingSession).filter(
        TrainingSession.id == session_id,
        TrainingSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(session, key, value)

    db.commit()
    db.refresh(session)
    return session


@router.delete("/{session_id}", status_code=204)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(TrainingSession).filter(
        TrainingSession.id == session_id,
        TrainingSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    db.delete(session)
    db.commit()