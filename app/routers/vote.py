# 3rd Party
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

# Project's modules
from ..schemas import VoteModel, ResponsePostPartModel
from ..database import get_db
from ..models import Vote, User, Post
from ..oath2 import get_current_user
from ..utils import get_row
from ..api_exceptions import *

__all__ = ["vote_router"]

vote_router = APIRouter(prefix="/vote", tags=["Vote"])


@vote_router.post("/", response_model=ResponsePostPartModel, status_code=status.HTTP_201_CREATED)
def set_vote(vote: VoteModel, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    post_id = vote.post_id
    is_like: bool = (lambda: True if vote.vote_status.value == "like" else False)()
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise PostNotFoundException(post_id=post_id)

    vote_row = get_row(user_id, post_id, db=db)

    if vote_row and is_like:
        raise UserAlreadyVotedException(user_id=user_id, post_id=post_id)

    if not vote_row and not is_like:
        raise LikeNotExistingPostException(user_id=user_id, post_id=post_id)

    if vote_row and not is_like:
        db.delete(vote_row)

    elif not vote_row and is_like:
        vote_row = Vote(user_id=user_id, post_id=post_id)
        db.add(vote_row)

    db.commit()
    return post
