from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, database

router = APIRouter(prefix="/songs")


@router.get("/{song_id}", response_model=schemas.SongOut)
def read_song(song_id: int, db: Session = Depends(database.get_db)):
    song = crud.get_song(db, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@router.get("/", response_model=list[schemas.SongOut])
def read_songs(
    skip: int = 0, limit: int = 10, db: Session = Depends((database.get_db))
):
    return crud.get_songs(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.SongOut)
def create_song(song: schemas.SongCreate, db: Session = Depends(database.get_db)):
    return crud.create_song(db, song)


@router.put("/{song_id}", response_model=schemas.SongOut)
def update_song(
    song_id: int, song: schemas.SongUpdate, db: Session = Depends(database.get_db)
):
    updated_song = crud.update_song(db, song_id, song)
    if not updated_song:
        raise HTTPException(status_code=404, detail="Song not found")
    return updated_song


@router.delete("/{song_id}", response_model=schemas.SongOut)
def delete_song(song_id: int, db: Session = Depends(database.get_db)):
    deleted_song = crud.delete_song(db, song_id)
    if not deleted_song:
        raise HTTPException(status_code=404, detail="song not found")
    return deleted_song
