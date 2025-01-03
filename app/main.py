from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, database, models, schemas

app = FastAPI()
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@router.post("/songs", response_model=schemas.SongOut)
def create_song(song: schemas.SongCreate, db: Session = Depends(database.get_db)):
    return crud.create_song(db, song)


@router.get("/songs/{song_id}", response_model=schemas.SongOut)
def read_song(song_id: int, db: Session = Depends(database.get_db)):
    song = crud.get_song(db, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@router.get("/songs/", response_model=list[schemas.SongOut])
def read_songs(
    skip: int = 0, limit: int = 10, db: Session = Depends((database.get_db))
):
    return crud.get_songs(db, skip=skip, limit=limit)


@router.put("/songs/{song_id}", response_model=schemas.SongOut)
def update_song(
    song_id: int, song: schemas.SongUpdate, db: Session = Depends(database.get_db)
):
    updated_song = crud.update_song(db, song_id, song)
    if not updated_song:
        raise HTTPException(status_code=404, detail="Song not found")
    return updated_song


@router.delete("songs/{song_id}", response_model=schemas.SongOut)
def delete_song(song_id: int, db: Session = Depends(database.get_db)):
    deleted_song = crud.delete_song(db, song_id)
    if not deleted_song:
        raise HTTPException(status_code=404, detail="song not found")
    return deleted_song
