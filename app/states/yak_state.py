import reflex as rx
from typing import TypedDict, Optional
import datetime
import uuid
import random


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
    is_owner: bool = False


class YakState(rx.State):
    peek_score: int = 137
    posts: list[Post] = [
        {
            "id": "1",
            "content": "Just saw a golden retriever riding a skateboard in SLU. Made my day.",
            "votes": 12,
            "created_at": "2 hours ago",
            "user_vote": 0,
            "is_owner": False,
            "comments": [
                {
                    "id": "c1",
                    "content": "No way! I think I saw that too!",
                    "created_at": "1 hour ago",
                },
                {
                    "id": "c2",
                    "content": "Pics or it didn't happen.",
                    "created_at": "30 minutes ago",
                },
            ],
        },
        {
            "id": "2",
            "content": "Anyone know if the new coffee shop on 9th is any good? The line is always so long.",
            "votes": 5,
            "created_at": "5 hours ago",
            "user_vote": 0,
            "comments": [],
            "is_owner": False,
        },
        {
            "id": "3",
            "content": "That awkward moment when you hold the door for someone and they're just a little too far away.",
            "votes": 27,
            "created_at": "1 day ago",
            "user_vote": 0,
            "is_owner": False,
            "comments": [
                {
                    "id": "c3",
                    "content": "Happens to me all the time.",
                    "created_at": "20 hours ago",
                }
            ],
        },
    ]
    show_create_dialog: bool = False
    new_post_content: str = ""
    new_comment_content: str = ""
    sort_by: str = "hot"

    @rx.var
    def sorted_posts(self) -> list[Post]:
        if self.sort_by == "new":
            return sorted(
                self.posts,
                key=lambda p: self.post_age_seconds(p["created_at"]),
                reverse=False,
            )
        return sorted(self.posts, key=lambda p: p["votes"], reverse=True)

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

    post_detail: Post | None = None

    @rx.event
    def get_post_by_id(self):
        post_id = self.router.page.params.get("post_id")
        if not post_id:
            self.post_detail = None
            return
        for post in self.posts:
            if post["id"] == post_id:
                self.post_detail = post
                return
        self.post_detail = None

    @rx.event
    def clear_post_detail(self):
        self.post_detail = None

    @rx.event
    def toggle_create_dialog(self):
        self.show_create_dialog = not self.show_create_dialog
        self.new_post_content = ""

    @rx.event
    def create_post(self):
        if not self.is_post_invalid:
            new_post: Post = {
                "id": str(uuid.uuid4()),
                "content": self.new_post_content,
                "votes": 1,
                "created_at": "Just now",
                "user_vote": 1,
                "comments": [],
                "is_owner": True,
            }
            self.posts.insert(0, new_post)
            self.show_create_dialog = False
            self.new_post_content = ""
            self.peek_score += 10
            return rx.toast(
                title="Yak Posted!",
                description="+10 to your Peek Score!",
                duration=3000,
            )

    @rx.event
    def add_comment(self, post_id: str):
        if not self.is_comment_invalid:
            for i, post in enumerate(self.posts):
                if post["id"] == post_id:
                    new_comment: Comment = {
                        "id": str(uuid.uuid4()),
                        "content": self.new_comment_content,
                        "created_at": "Just now",
                    }
                    self.posts[i]["comments"].append(new_comment)
                    if self.post_detail and self.post_detail["id"] == post_id:
                        self.post_detail["comments"].append(new_comment)
                    self.new_comment_content = ""
                    return rx.toast(
                        title="Comment Added",
                        description="Someone will see your reply.",
                        duration=3000,
                    )

    @rx.event
    def handle_vote(self, post_id: str, vote_value: int):
        for i, post in enumerate(self.posts):
            if post["id"] == post_id:
                if post["user_vote"] == vote_value:
                    self.posts[i]["votes"] -= vote_value
                    self.posts[i]["user_vote"] = 0
                else:
                    self.posts[i]["votes"] -= post["user_vote"]
                    self.posts[i]["votes"] += vote_value
                    self.posts[i]["user_vote"] = vote_value
                if self.post_detail and self.post_detail["id"] == post_id:
                    self.post_detail = self.posts[i]
                if vote_value == 1 and self.posts[i]["user_vote"] == 1:
                    self.peek_score += 1
                elif vote_value == -1 and self.posts[i]["user_vote"] == -1:
                    self.peek_score -= 1
                elif self.posts[i]["user_vote"] == 0:
                    self.peek_score += -vote_value
                return

    @rx.event
    def set_sort_by(self, sort_type: str):
        self.sort_by = sort_type

    @rx.event
    def post_age_seconds(self, created_at_str: str) -> int:
        if "Just now" in created_at_str:
            return 0
        if "minutes" in created_at_str or "minute" in created_at_str:
            return int(created_at_str.split()[0]) * 60
        if "hours" in created_at_str or "hour" in created_at_str:
            return int(created_at_str.split()[0]) * 3600
        if "days" in created_at_str or "day" in created_at_str:
            return int(created_at_str.split()[0]) * 86400
        return 9999999

    @rx.event
    def report_post(self, post_id: str):
        return rx.toast(
            title="Post Reported",
            description="Thanks for helping keep the community safe.",
            duration=4000,
        )

    @rx.event
    def delete_post(self, post_id: str):
        self.posts = [p for p in self.posts if p["id"] != post_id]
        self.peek_score -= 10
        if self.post_detail and self.post_detail["id"] == post_id:
            self.post_detail = None
            return rx.redirect("/")
        return rx.toast(
            title="Post Deleted",
            description="Your yak has been removed.",
            duration=3000,
        )