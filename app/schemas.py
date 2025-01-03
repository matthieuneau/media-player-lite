from pydantic import BaseModel, EmailStr
from typing import Optional


class PlaylistBase(BaseModel):
    name: str


class PlaylistCreate(PlaylistBase):
    pass


class PlaylistUpdate(BaseModel):
    name: Optional[str] = None


class PlaylistOut(PlaylistBase):
    id: int
    user_id: int

    class Config:
        model_config = {"from_attributes": True}


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserOut(UserBase):
    id: int
    password: Optional[str] = None

    class Config:
        model_config = {"from_attributes": True}


class SongBase(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    duration: Optional[int] = None
    genre: Optional[str] = None


class SongCreate(SongBase):
    pass


class SongUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    duration: Optional[str] = None
    genre: Optional[str] = None


class SongOut(SongBase):
    id: int

    class Config:
        model_config = {"from_attributes": True}
