from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum, func, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from .api_types import Category, Gender


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(column="users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey(column="posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)

    user = relationship("User")
    post = relationship("Post")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    category = Column(Enum(Category), nullable=False)
    score = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey(column="users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    registered_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
