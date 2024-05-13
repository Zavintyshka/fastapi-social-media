from enum import EnumType
from typing import Optional

from sqlalchemy.orm import Session

from .models import Vote


def convert_to_enum_obj(enum: EnumType, var: str) -> Optional[EnumType]:
    try:
        enum_obj = enum[var]
    except KeyError:
        return None
    return enum_obj


def get_row(user_id: int, post_id: int, db: Session) -> Optional[Vote]:
    """"Returns Vote row if exists with the specific user_id and post_id, else None"""
    row = db.query(Vote).filter(Vote.user_id == user_id, Vote.post_id == post_id).first()
    return row if row else None


if __name__ == "__main__":
    pass
