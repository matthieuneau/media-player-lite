from typing import Optional
from app.models import User, Song, Playlist
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app import schemas


def get_all_playlists(db: Session):
    return db.query(Playlist).all()


def get_playlists_by_user(db: Session, user_id: int):
    return db.query(Playlist).filter(Playlist.user_id == user_id).all()


def create_playlist(db: Session, playlist: schemas.PlaylistCreate, user_id: int):
    db_playlist = Playlist(name=playlist.name, user_id=user_id)
    db.add(db_playlist)
    try:
        db.commit()
    except Exception:
        db.rollback()
    db.refresh(db_playlist)
    return db_playlist


def get_playlist(db: Session, playlist_id: int):
    return db.query(Playlist).filter(Playlist.id == playlist_id).first()


def update_playlist(
    db: Session, playlist: Playlist, playlist_update: schemas.PlaylistUpdate
):
    if playlist_update.name:
        playlist.name = playlist_update.name
    try:
        db.commit()
    except Exception:
        db.rollback()
    db.refresh(playlist)
    return playlist


def delete_playlist(db: Session, playlist: Playlist):
    db.delete(playlist)
    db.commit()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    try:
        db.commit()
    except Exception:
        db.rollback()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, user_email: EmailStr) -> Optional[User]:
    return db.query(User).filter(User.email == user_email).first()


def get_all_users(db: Session):
    return db.query(User).all()


def create_song(db: Session, song: schemas.SongCreate):
    db_song = Song(**song.dict())
    db.add(db_song)
    try:
        db.commit()
    except Exception:
        db.rollback()
    db.refresh(db_song)
    return db_song


def get_song(db: Session, song_id: int):
    return db.query(Song).filter(Song.id == song_id).first()


def get_songs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Song).offset(skip).limit(limit).all()


def update_song(db: Session, song_id: int, song_data: schemas.SongUpdate):
    db_song = db.query(Song).filter(Song.id == song_id).first()
    if not db_song:
        return None
    for key, value in song_data.dict(exclude_unset=True).items():
        setattr(db_song, key, value)
    try:
        db.commit()
    except Exception:
        db.rollback()
    db.refresh(db_song)
    return db_song


def delete_song(db: Session, song_id: int):
    db_song = db.query(Song).filter(Song.id == song_id).first()
    if not db_song:
        return None
    db.delete(db_song)
    try:
        db.commit()
    except Exception:
        db.rollback()
    db.refresh(db_song)
    return db_song
