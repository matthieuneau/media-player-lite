from datetime import datetime
from sqlalchemy import (
    TIMESTAMP,
    ForeignKey,
    Integer,
    String,
    func,
    Table,
    Column,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )
    playlists: Mapped["Playlist"] = relationship("Playlist", back_populates="user")


class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    artist = Column(String(100), nullable=False)
    album = Column(String(100), nullable=True)
    duration = Column(Integer, nullable=True)
    genre = Column(String(50), nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


playlist_songs = Table(
    "playlist_songs",
    Base.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id"), primary_key=True),
    Column("song_id", Integer, ForeignKey("songs.id"), primary_key=True),
    Column("added_at", TIMESTAMP, server_default=func.now()),
)


class Playlist(Base):
    __tablename__ = "playlists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship("User", back_populates="playlists")
    songs: Mapped[list["Song"]] = relationship(
        "Song", secondary=playlist_songs, backref="playlists"
    )
