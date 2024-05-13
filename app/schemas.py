from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr
from .api_types import Category, Gender, Vote


# Users
class UserBaseModel(BaseModel):
    email: EmailStr
    password: str
    firstname: str
    lastname: str
    age: Optional[int] = None
    gender: Optional[Gender] = None
    # also id & registered_at fields in DB


class CreateUserModel(UserBaseModel):
    pass


class ResponseUserModel(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    age: Optional[int] = None
    gender: Optional[Gender] = None

    class Config:
        from_attributes = True


# Posts
class PostBaseModel(BaseModel):
    title: str
    text: str
    category: Category
    score: int
    # also id & created_at & user_id fields in DB


class CreatePostModel(PostBaseModel):
    pass


class UpdatePostModel(PostBaseModel):
    pass


class ResponsePostPartModel(PostBaseModel):
    id: int
    created_at: datetime
    owner: ResponseUserModel

    class Config:
        from_attributes = True


class ResponsePostModelFull(BaseModel):
    Post: ResponsePostPartModel
    likes: int


# Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
    expire_time: datetime


# Vote

class VoteModel(BaseModel):
    post_id: int
    vote_status: Vote
