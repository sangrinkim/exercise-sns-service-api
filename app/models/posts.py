from pydantic import BaseModel

from app.models.common import ModifiyDateTime


# 사진파일 정보
class PhotoFileInfo(ModifiyDateTime):
    file_no: int
    original_file_name: str
    save_file_name: str


# 댓글
class CommentBase(BaseModel):
    content: str

class Comment(ModifiyDateTime, CommentBase):
    post_id: str
    comment_id: str


# 게시물
class Post(ModifiyDateTime):
    post_id: str
    exercise_code: str
    photos: list[PhotoFileInfo]
    comments: list[Comment] = []


class PostOut(Post):
    prev_post_id: str = None
    next_post_id: str = None


# 게시물 목록
class Posts(BaseModel):
    count: int
    items: list[Post]