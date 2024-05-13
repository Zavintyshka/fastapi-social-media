from typing import List

# 3rd Party
from fastapi import Depends, APIRouter, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

# Project's modules
from ..database import get_db
from ..models import Post, User, Vote
from ..schemas import CreatePostModel, UpdatePostModel, ResponsePostPartModel, ResponsePostModelFull
from ..oath2 import get_current_user
from ..api_types import Category
from ..utils import convert_to_enum_obj
from ..api_exceptions import *

__all__ = ["post_router"]

post_router = APIRouter(prefix="/posts", tags=["Post"])


@post_router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponsePostPartModel)
def create_post(post: CreatePostModel, db: Session = Depends(get_db),
                user: User = Depends(get_current_user)):
    new_post = Post(user_id=user.id, **dict(post))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@post_router.get("/", response_model=List[ResponsePostModelFull])
def get_posts(db: Session = Depends(get_db),
              contains: str = '',
              category: str = None,
              limit: int = 10,
              offset: int = 0):
    posts_query: Query = db.query(Post, func.COUNT(Vote.user_id).label("likes"))

    if category := convert_to_enum_obj(Category, category):
        posts_query = posts_query.filter(Post.category == category)

    posts_query = posts_query.filter(Post.title.contains(contains))

    posts_query = posts_query.join(Vote, Post.id == Vote.post_id, isouter=True).group_by(Post.id).order_by(
        Post.id.asc())

    posts_query = posts_query.limit(limit).offset(offset)
    posts = posts_query.all()
    if not posts:
        raise EmptyListOfPostsException()
    return posts


@post_router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=ResponsePostModelFull)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post, func.COUNT(Vote.user_id).label("likes")).join(Vote, Post.id == Vote.post_id,
                                                                        isouter=True).filter(
        Post.id == post_id).group_by(Post.id).first()
    if not post:
        raise PostNotFoundException(post_id=post_id)
    return post


@post_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post_query: Query = db.query(Post).filter(Post.id == post_id)
    post = post_query.first()
    if not post:
        raise PostNotFoundException(post_id=post_id)

    if post.user_id != user.id:
        raise DeletePostException()

    post_query.delete()
    db.commit()


@post_router.put("/{post_id}", status_code=status.HTTP_200_OK, response_model=ResponsePostPartModel)
def update_post_by_put(post_id: int, updated_post: UpdatePostModel, db: Session = Depends(get_db),
                       user: User = Depends(get_current_user)):
    post_query: Query = db.query(Post).filter(Post.id == post_id)
    db_post = post_query.first()
    if not db_post:
        raise PostNotFoundException(post_id=post_id)
    if db_post.user_id != user.id:
        raise UpdatePostException()

    post_query.update(dict(updated_post), synchronize_session=False)
    db.commit()
    return post_query.first()
