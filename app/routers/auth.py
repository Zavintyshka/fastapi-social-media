# 3rd Party
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Project's modules
from ..database import get_db
from ..models import User
from ..security import is_password_legit
from ..oath2 import create_access_token
from ..schemas import Token
from ..api_exceptions import *

__all__ = ["auth_router"]

auth_router = APIRouter(tags=["Authentication"])


@auth_router.post("/login", response_model=Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email, password = user_credential.username, user_credential.password
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise UserNotFoundLoginException(user_email=email)

    if not is_password_legit(password, user.password):
        raise WrongPasswordException()

    jwt = create_access_token(payload={"user_id": user.id})

    return {"access_token": jwt, "token_type": "bearer"}
