from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, database
from app import schemas
from app.schemas import UserOut, UserUpdate, UserCreate
from passlib.context import CryptContext
from app.auth import TokenResponse, create_access_token, get_current_user

router = APIRouter(prefix="/users")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register/", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(database.get_db)):
    if crud.get_user_by_email(db, user_email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    return crud.create_user(db, user)


@router.post(
    "/login/",
    response_model=TokenResponse,
    status_code=200,
    summary="Authenticate users",
    description="Authenticate a user using their email and password. Returns a JSON Web Token (JWT) that can be used to access protected endpoints.",
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = crud.get_user_by_email(db, user_email=form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# TODO: make sure only admins can trigger this
@router.get("/", response_model=UserOut)
def list_users(db: Session = Depends(database.get_db)):
    users = crud.get_all_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users


@router.get(
    "/me/",
    response_model=UserOut,
    summary="Get Current User",
    description="Retrieve the details of the currently authenticated user.",
    tags=["Users"],
)
def get_user_me(
    current_user: UserOut = Depends(get_current_user),
):
    return current_user


@router.delete(
    "/me/",
    summary="Delete Current User",
    description="Delete the authenticated user's account permanently.",
    tags=["Users"],
)
def delete_user_me(
    db: Session = Depends(database.get_db),
    current_user: UserOut = Depends(get_current_user),
):
    db.delete(current_user)
    try:
        db.commit()
    except Exception:
        db.rollback()
    return {"message": "User account deleted successfully"}


@router.put(
    "/me/",
    response_model=UserOut,
    summary="Update current user",
    description="Update the authenticated user's profile information",
    tags=["Users"],
)
def update_user_me(
    user_update: UserUpdate,
    db: Session,
    current_user: UserOut = Depends(get_current_user),
):
    if user_update.username:
        current_user.username = user_update.username
    if user_update.email:
        if crud.get_user_by_email(db, user_email=user_update.email):
            raise HTTPException(status_code=400, detail="email already in use")
        current_user.email = user_update.email
    if user_update.password:
        current_user.password = pwd_context.hash(user_update.password)

    db.add(current_user)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database commit failed")
    db.refresh(current_user)
    return schemas.UserOut.model_validate(current_user)
