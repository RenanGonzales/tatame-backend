# app/api/routes/games.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Game, User
from app.schemas.game import GameCreate, GameUpdate, GameResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/", response_model=list[GameResponse])
def list_games(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Game).filter(Game.user_id == current_user.id).all()


@router.post("/", response_model=GameResponse, status_code=201)
def create_game(
    data: GameCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    game = Game(name=data.name, user_id=current_user.id)
    db.add(game)
    db.commit()
    db.refresh(game)
    return game


@router.put("/{game_id}", response_model=GameResponse)
def update_game(
    game_id: int,
    data: GameUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    game = db.query(Game).filter(
        Game.id == game_id,
        Game.user_id == current_user.id
    ).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(game, key, value)

    db.commit()
    db.refresh(game)
    return game


@router.delete("/{game_id}", status_code=204)
def delete_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    game = db.query(Game).filter(
        Game.id == game_id,
        Game.user_id == current_user.id
    ).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    db.delete(game)
    db.commit()