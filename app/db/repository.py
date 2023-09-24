from abc import ABC, abstractmethod

from app.models.common import ExerciseTypes
from app.models.posts import CommentBase, PhotoFileInfo, Post, PostOut, Posts
from app.models.users import User, UserInDB


# 데이터 베이스 인터페이스 정의
class Repository(ABC):
    def __init__(self, repository_name):
        self.repository_name = repository_name


    # 사용자 정보 가져오기
    @abstractmethod
    def get_user(self, username: str) -> UserInDB:
        pass


    # 운동 유형 가져오기
    @abstractmethod
    def get_exercise_types(self) -> ExerciseTypes:
        pass


    # 운동 게시물 등록
    @abstractmethod
    def create_exercise_post(self, exercise_code: str, photos: list[PhotoFileInfo]) -> str:
        pass


    # 운동 목록 가져오기
    @abstractmethod
    def get_exercise_posts(self, sort_comment_time: bool = False, order_desc: bool = True, filter_exercise_codes: list[str] = None) -> Posts:
        pass


    # 운동 게시물 가져오기
    @abstractmethod
    def get_exercise_post(self, post_id) -> Post:
        pass

    # 운동 게시물(이전/다음 포함용) 가져오기
    @abstractmethod
    def get_exercise_post_out(self, post_id) -> PostOut:
        pass


    # 댓글 등록
    @abstractmethod
    def create_comment(self, post_id: str, comment: CommentBase) -> str:
        pass


    # 게시물 삭제
    @abstractmethod
    def delete_exercise_post(self, post_id):
        pass