import reflex as rx
from typing import TypedDict, Optional
import datetime
import uuid
from sqlmodel import Session, select, delete
from app.db.database import get_db_session
from app.db import models


class Comment(TypedDict):
    id: str
    content: str
    created_at: str


class Post(TypedDict):
    id: str
    content: str
    votes: int
    created_at: str
    user_vote: int
    comments: list[Comment]
    is_owner: bool


def time_since(dt: datetime.datetime) -> str:
    now = datetime.datetime.utcnow()
    diff = now - dt
    seconds = diff.total_seconds()
    if seconds < 60:
        return "Just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{('s' if minutes > 1 else '')} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{('s' if hours > 1 else '')} ago"
    else:
        days = int(seconds / 86400)
        return f"{days} day{('s' if days > 1 else '')} ago"


class YakState(rx.State):
    peek_score: int = 137
    posts: list[Post] = []
    show_create_dialog: bool = False
    new_post_content: str = ""
    new_comment_content: str = ""
    sort_by: str = "hot"
    post_detail: Post | None = None

    def _get_session_id(self) -> str:
        return self.router.session.session_id

    def _format_post_for_frontend(
        self, post_model: models.Post, session: Session
    ) -> Post:
        session_id = self._get_session_id()
        user_vote_model = session.exec(
            select(models.UserVote).where(
                models.UserVote.post_id == post_model.id,
                models.UserVote.user_session_id == session_id,
            )
        ).first()
        user_vote = user_vote_model.vote_value if user_vote_model else 0
        comments = sorted(post_model.comments, key=lambda c: c.created_at, reverse=True)
        return {
            "id": post_model.id,
            "content": post_model.content,
            "votes": post_model.votes,
            "created_at": time_since(post_model.created_at),
            "user_vote": user_vote,
            "comments": [
                {
                    "id": c.id,
                    "content": c.content,
                    "created_at": time_since(c.created_at),
                }
                for c in comments
            ],
            "is_owner": post_model.owner_session_id == session_id,
        }

    @rx.event
    def load_posts(self):
        with get_db_session() as session:
            posts_query = select(models.Post)
            if self.sort_by == "new":
                posts_query = posts_query.order_by(models.Post.created_at.desc())
            else:
                posts_query = posts_query.order_by(models.Post.votes.desc())
            post_models = session.exec(posts_query).all()
            self.posts = [
                self._format_post_for_frontend(p, session) for p in post_models
            ]

    @rx.var
    def char_count(self) -> int:
        return len(self.new_post_content)

    @rx.var
    def is_post_invalid(self) -> bool:
        return self.char_count == 0 or self.char_count > 200

    @rx.var
    def comment_char_count(self) -> int:
        return len(self.new_comment_content)

    @rx.var
    def is_comment_invalid(self) -> bool:
        return self.comment_char_count == 0 or self.comment_char_count > 150

    @rx.event
    def get_post_by_id(self):
        post_id = self.router.page.params.get("post_id")
        if not post_id:
            self.post_detail = None
            return
        with get_db_session() as session:
            post_model = session.get(models.Post, post_id)
            if post_model:
                self.post_detail = self._format_post_for_frontend(post_model, session)
            else:
                self.post_detail = None

    @rx.event
    def clear_post_detail(self):
        self.post_detail = None

    @rx.event
    def create_post(self):
        if self.is_post_invalid:
            return
        with get_db_session() as session:
            session_id = self._get_session_id()
            new_post_model = models.Post(
                content=self.new_post_content, owner_session_id=session_id
            )
            session.add(new_post_model)
            session.flush()
            new_vote = models.UserVote(
                post_id=new_post_model.id, user_session_id=session_id, vote_value=1
            )
            session.add(new_vote)
            session.commit()
        self.show_create_dialog = False
        self.new_post_content = ""
        self.peek_score += 10
        yield YakState.load_posts
        return rx.toast(
            title="Yak Posted!", description="+10 to your Peek Score!", duration=3000
        )

    @rx.event
    async def add_comment(self, post_id: str):
        if self.is_comment_invalid:
            return
        with get_db_session() as session:
            session_id = self._get_session_id()
            new_comment_model = models.Comment(
                post_id=post_id,
                content=self.new_comment_content,
                owner_session_id=session_id,
            )
            session.add(new_comment_model)
            session.commit()
        self.new_comment_content = ""
        yield YakState.get_post_by_id()
        yield rx.toast(
            title="Comment Added",
            description="Someone will see your reply.",
            duration=3000,
        )
        return

    @rx.event
    def handle_vote(self, post_id: str, vote_value: int):
        with get_db_session() as session:
            session_id = self._get_session_id()
            post_model = session.get(models.Post, post_id)
            if not post_model:
                return
            existing_vote = session.exec(
                select(models.UserVote).where(
                    models.UserVote.post_id == post_id,
                    models.UserVote.user_session_id == session_id,
                )
            ).first()
            if existing_vote:
                if existing_vote.vote_value == vote_value:
                    post_model.votes -= vote_value
                    self.peek_score += -vote_value
                    session.delete(existing_vote)
                else:
                    post_model.votes -= existing_vote.vote_value
                    post_model.votes += vote_value
                    self.peek_score += 2 * vote_value
                    existing_vote.vote_value = vote_value
                    session.add(existing_vote)
            else:
                post_model.votes += vote_value
                self.peek_score += vote_value
                new_vote = models.UserVote(
                    post_id=post_id, user_session_id=session_id, vote_value=vote_value
                )
                session.add(new_vote)
            session.commit()
        if self.post_detail and self.post_detail["id"] == post_id:
            yield YakState.get_post_by_id()
        yield YakState.load_posts

    @rx.event
    def set_sort_by(self, sort_type: str):
        self.sort_by = sort_type
        return YakState.load_posts

    @rx.event
    def report_post(self, post_id: str):
        return rx.toast(
            title="Post Reported",
            description="Thanks for helping keep the community safe.",
            duration=4000,
        )

    @rx.event
    async def delete_post(self, post_id: str):
        with get_db_session() as session:
            session_id = self._get_session_id()
            post_to_delete = session.get(models.Post, post_id)
            if post_to_delete and post_to_delete.owner_session_id == session_id:
                session.exec(
                    delete(models.Comment).where(models.Comment.post_id == post_id)
                )
                session.exec(
                    delete(models.UserVote).where(models.UserVote.post_id == post_id)
                )
                session.delete(post_to_delete)
                session.commit()
                self.peek_score -= 10
                is_detail_view = self.post_detail and self.post_detail["id"] == post_id
                yield YakState.load_posts
                if is_detail_view:
                    yield rx.redirect("/")
                yield rx.toast(
                    title="Post Deleted",
                    description="Your yak has been removed.",
                    duration=3000,
                )
            else:
                yield rx.toast(
                    title="Error", description="You can only delete your own posts."
                )