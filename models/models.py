from typing import Any, Dict

from sqlalchemy import String, Integer, ForeignKey, Boolean, MetaData
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from config.settings import settings


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(schema=settings.db.current_schema)


class GameObject(Base):
    __tablename__ = 'game_objects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, default='void')
    pos_x: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pos_y: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_solid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_collectable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_consumable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    action: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False, default={"action": "do_nothing", "params": [0]})
    hp: Mapped[int] = mapped_column(Integer, nullable=False, default=-999)
    char_stats_id: Mapped[int] = mapped_column(Integer, ForeignKey('char_stats.id', ondelete='CASCADE'))

    char_stats = relationship("CharStats", back_populates="inventory")


class CharStats(Base):
    __tablename__ = "char_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[int] = mapped_column(ForeignKey("characters.id"), unique=True)
    health: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    energy: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    hungry: Mapped[int]
    position_x: Mapped[int]
    position_y: Mapped[int]
    location_id: Mapped[str]
    attack_modifier: Mapped[int]
    attack_damage: Mapped[int]
    defence: Mapped[int]
    is_dead: Mapped[bool] = mapped_column(default=False)

    character: Mapped["Character"] = relationship(
        "Character",
        back_populates="stats",
        uselist=False
    )
    inventory: Mapped[list["GameObject"]] = relationship(
        "GameObject",
        back_populates="char_stats",
        cascade="all, delete-orphan"
    )


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    user_id: Mapped[str | None] = mapped_column(String(120))

    stats: Mapped["CharStats"] = relationship(
        "CharStats",
        back_populates="character",
        uselist=False
    )
