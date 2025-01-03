from sqlalchemy.orm import Session
from app import models, schemas


def create_song(db: Session, song: schemas.SongCreate):
    db_song = models.Song(**song.dict())
    db.add(db_song)
    try:
        db.commit()
    except Exception:
        db.rollback()
    db.refresh(db_song)
    return db_song


def get_song(db: Session, song_id: int):
    return db.query(models.Song).filter(models.Song.id == song_id).first()


def get_songs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Song).offset(skip).limit(limit).all()


def update_song(db: Session, song_id: int, song_data: schemas.SongUpdate):
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
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
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if not db_song:
        return None
    db.delete(db_song)
    try:
        db.commit()
    except Exception:
        db.rollback()
    db.refresh(db_song)
    return db_song
