from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database
from app.auth import get_current_user

router = APIRouter(prefix="/playlists")


@router.get(
    "/",
    response_model=List[schemas.PlaylistOut],
    summary="Get All Playlists",
    description="Fetch all playlists in the database.",
    tags=["Playlists"],
)
def get_all_playlists(db: Session = Depends(database.get_db)):
    return crud.get_all_playlists(db)


@router.get(
    "/mine/",
    response_model=List[schemas.PlaylistOut],
    summary="Get My Playlists",
    description="Fetch all playlists created by the currently authenticated user.",
    tags=["Playlists"],
)
def get_user_playlists(
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(database.get_db),
):
    return crud.get_playlists_by_user(db, user_id=current_user.id)


@router.post(
    "/",
    response_model=schemas.PlaylistOut,
    summary="Create Playlist",
    description="Create a new playlist for the authenticated user.",
    tags=["Playlists"],
)
def create_playlist(
    playlist: schemas.PlaylistCreate,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(database.get_db),
):
    return crud.create_playlist(db, playlist, user_id=current_user.id)


@router.get(
    "/{playlist_id}/",
    response_model=schemas.PlaylistOut,
    summary="Get Playlist Details",
    description="Fetch details of a specific playlist, including its songs.",
    tags=["Playlists"],
)
def get_playlist(playlist_id: int, db: Session = Depends(database.get_db)):
    playlist = crud.get_playlist(db, playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist


@router.put(
    "/{playlist_id}/",
    response_model=schemas.PlaylistOut,
    summary="Update Playlist",
    description="Update the name of a playlist.",
    tags=["Playlists"],
)
def update_playlist(
    playlist_id: int,
    playlist_update: schemas.PlaylistUpdate,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(database.get_db),
):
    playlist = crud.get_playlist(db, playlist_id=playlist_id)
    if not playlist or playlist.user_id != current_user.id:
        raise HTTPException(
            status_code=404, detail="Playlist not found or unauthorized"
        )
    return crud.update_playlist(db, playlist, playlist_update)


@router.delete(
    "/{playlist_id}/",
    summary="Delete Playlist",
    description="Delete a playlist owned by the authenticated user.",
    tags=["Playlists"],
)
def delete_playlist(
    playlist_id: int,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(database.get_db),
):
    playlist = crud.get_playlist(db, playlist_id=playlist_id)
    if not playlist or playlist.user_id != current_user.id:
        raise HTTPException(
            status_code=404, detail="Playlist not found or unauthorized"
        )
    crud.delete_playlist(db, playlist)
    return {"message": "Playlist deleted successfully"}
