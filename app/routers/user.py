from typing import List

# 3rd Party
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session

# Project's modules
from ..database import get_db
from ..models import User
from ..schemas import CreateUserModel, ResponseUserModel
from ..security import hash_password
from ..api_exceptions import *

__all__ = ["user_router"]

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.post("/", response_model=ResponseUserModel, status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUserModel, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    new_user = User(**dict(user))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user_router.get("/", response_model=List[ResponseUserModel])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise EmptyListOfUsersException()
    return users


@user_router.get("/{user_id}", response_model=ResponseUserModel)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException(user_id=user_id)
    return user
