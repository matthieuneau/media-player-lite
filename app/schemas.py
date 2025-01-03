from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


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
        orm_mode = True
