# app/models/models.py

import enum
from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, Text, Date, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class BeltRank(str, enum.Enum):
    white = "white"
    gray = "gray"
    yellow = "yellow"
    orange = "orange"
    green = "green"
    blue = "blue"
    purple = "purple"
    brown = "brown"
    black = "black"


class CardType(str, enum.Enum):
    takedown = "takedown"
    guard_pass = "guard_pass"
    sweep = "sweep"
    attack = "attack"
    recovery = "recovery"
    control = "control"
    defense = "defense"

class CardPerspective(str, enum.Enum):
    top = "top"
    bottom = "bottom"
    neutral = "neutral"

class CardContext(str, enum.Enum):
    gi = "gi"
    nogi = "nogi"
    mma = "mma"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    belt = Column(Enum(BeltRank), nullable=False, default=BeltRank.white)
    stripes = Column(SmallInteger, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())
    games = relationship("Game", back_populates="user", cascade="all, delete")

    deck = relationship("Deck", back_populates="user", cascade="all, delete")
    training_sessions = relationship("TrainingSession", back_populates="user", cascade="all, delete")

class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    name_en = Column(String(100), nullable=False)
    name_pt = Column(String(100), nullable=False)
    hierarchy_level = Column(SmallInteger, nullable=False, default=0)
    display_order = Column(SmallInteger, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())

    cards = relationship("Card", back_populates="position", cascade="all, delete")

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    position_id = Column(Integer, ForeignKey("positions.id", ondelete="CASCADE"))
    name_en = Column(String(100), nullable=False)
    name_pt = Column(String(100), nullable=False)
    type = Column(Enum(CardType), nullable=False)
    context = Column(Enum(CardContext), nullable=False, default=CardContext.gi)
    minimum_belt = Column(Enum(BeltRank), nullable=False, default=BeltRank.white)
    notes_en = Column(Text)
    notes_pt = Column(Text)
    illustration_url = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    perspective = Column(Enum(CardPerspective, name='cardperspective'), nullable=True, default=CardPerspective.neutral)

    position = relationship("Position", back_populates="cards")
    deck_entries = relationship("Deck", back_populates="card", cascade="all, delete")
    training_cards = relationship("TrainingCard", back_populates="card", cascade="all, delete")


class Deck(Base):
    __tablename__ = "deck"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"))
    favorited = Column(Boolean, default=False)
    rusty = Column(Boolean, default=False)
    studying = Column(Boolean, default=False)
    slot_order = Column(SmallInteger, default=0)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"))
    game = relationship("Game", back_populates="deck")

    __table_args__ = (UniqueConstraint("user_id", "card_id"),)

    user = relationship("User", back_populates="deck")
    card = relationship("Card", back_populates="deck_entries")


class TrainingSession(Base):
    __tablename__ = "training_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False, server_default=func.current_date())
    duration_min = Column(SmallInteger)
    result = Column(String(20))
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="training_sessions")
    training_cards = relationship("TrainingCard", back_populates="training_session", cascade="all, delete")


class TrainingCard(Base):
    __tablename__ = "training_cards"

    id = Column(Integer, primary_key=True)
    training_session_id = Column(Integer, ForeignKey("training_sessions.id", ondelete="CASCADE"))
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"))

    __table_args__ = (UniqueConstraint("training_session_id", "card_id"),)

    training_session = relationship("TrainingSession", back_populates="training_cards")
    card = relationship("Card", back_populates="training_cards")

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="games")
    deck = relationship("Deck", back_populates="game", cascade="all, delete")