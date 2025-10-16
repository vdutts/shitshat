from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
import datetime
import uuid


class Post(SQLModel, table=True):
    id: str = Field(default_factory=uuid.uuid4, primary_key=True)
    content: str
    votes: int = Field(default=1)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    owner_session_id: str = Field(index=True)
    comments: list["Comment"] = Relationship(back_populates="post")
    user_votes: list["UserVote"] = Relationship(back_populates="post")


class Comment(SQLModel, table=True):
    id: str = Field(default_factory=uuid.uuid4, primary_key=True)
    content: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    post_id: str = Field(foreign_key="post.id")
    owner_session_id: str = Field(index=True)
    post: Post = Relationship(back_populates="comments")


class UserVote(SQLModel, table=True):
    id: str = Field(default_factory=uuid.uuid4, primary_key=True)
    post_id: str = Field(foreign_key="post.id")
    user_session_id: str = Field(index=True)
    vote_value: int
    post: Post = Relationship(back_populates="user_votes")