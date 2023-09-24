from datetime import datetime
import operator

from app.models.common import COMMON_CODE_EXERCISE_TYPE, ExerciseType, ExerciseTypes
from app.models.posts import Comment, CommentBase, Post, PhotoFileInfo, PostOut, Posts
from app.db.repository import Repository
from app.models.users import User, UserInDB


# 사용자 샘플 데이터
fake_users_data = {
    "kimpro": {
        "username": "kimpro",
        "hashed_password": "$2y$10$ZTAVbmMp99MapGgiXYDfXebptjtl36u8Rr8/9rhuT08CCkxlhfyKq",
        "permission": "manager"
    },
    "fittrix": {
        "username": "fittrix",
        "hashed_password": "$2y$10$LQ4mjpvXLBUSLCNkNLW9PuNupsObokbc2u1kamuxG.N3cFm7nsqei",
        "permission": "manager"
    }, 
    "james": {
        "username": "james",
        "hashed_password": "$2y$10$942uhgNrozwc/yH92Vo1gO6Y8nqolfmWB0Nm8djCrevTj1WHd58Qa",
        "permission": "user"
    },
    "david": {
        "username": "david",
        "hashed_password": "$2y$10$HvJwDlwg.0nY4BR0pVhxSuef/XoKG6qPKU3dpnK6cfNgzcilFlCWi",
        "permission": "user"
    }
}


# 운동 유형 샘플 데이터
fake_exercise_types_data = {
    "squat": "스쿼트",
    "lunge": "런지",
    "bench_press": "벤치 프레스",
    "running": "런닝",
    "other": "기타"
}

# 운동 게시물 샘플 데이터
fake_exercise_posts_data = {
    '1': Post(created_time=datetime(2023, 9, 23, 20, 8, 44, 671192), updated_time=datetime(2023, 9, 23, 20, 8, 44, 671193), post_id='1', exercise_code='lunge', photos=[PhotoFileInfo(created_time=datetime(2023, 9, 23, 20, 8, 44, 671117), updated_time=datetime(2023, 9, 23, 20, 8, 44, 671119), file_no=1, original_file_name='lunge.png', save_file_name='20230923-200844_lunge.png'), PhotoFileInfo(created_time=datetime(2023, 9, 23, 20, 8, 44, 671180), updated_time=datetime(2023, 9, 23, 20, 8, 44, 671181), file_no=2, original_file_name='lunge.jpg', save_file_name='20230923-200844_lunge.jpg')], comments=[]), 
    '2': Post(created_time=datetime(2023, 9, 23, 20, 9, 5, 908563), updated_time=datetime(2023, 9, 23, 20, 9, 5, 908564), post_id='2', exercise_code='lunge', photos=[PhotoFileInfo(created_time=datetime(2023, 9, 23, 20, 9, 5, 908492), updated_time=datetime(2023, 9, 23, 20, 9, 5, 908494), file_no=1, original_file_name='lunge.png', save_file_name='20230923-200905_lunge.png'), PhotoFileInfo(created_time=datetime(2023, 9, 23, 20, 9, 5, 908554), updated_time=datetime(2023, 9, 23, 20, 9, 5, 908555), file_no=2, original_file_name='lunge.jpg', save_file_name='20230923-200905_lunge.jpg')], comments=[Comment(content='두번째 게시물의 댓글입니다.', created_time=datetime(2023, 9, 24, 0, 30, 11, 671699), updated_time=datetime(2023, 9, 24, 0, 30, 11, 671703), post_id='2', comment_id='1')])
}


# 게시물 아이디 생성 -> 추후 빅데이터에 맞는 게시물 아이디를 생성을 위해 함수화
def create_post_id() -> str:
    return str(len(fake_exercise_posts_data) + 1)


# 댓글 아이디 생성 -> 추후 빅데이터에 맞는 댓글 아이디를 생성을 위해 함수화
def create_comment_id(post_id: str) -> str:
    return str(len(fake_exercise_posts_data[post_id].comments) + 1)


class FakeRepository(Repository):
    def __init__(self):
        super().__init__("Fake Repository for testing")


    # 사용자 정보 가져오기
    def get_user(self, username: str) -> UserInDB:
        user = fake_users_data.get(username)
        if not user:
            return None
        
        return UserInDB(**user)


    # 운동 유형 가져오기
    def get_exercise_types(self) -> ExerciseTypes:
        exercise_types = []
        for key in fake_exercise_types_data:
            exercise_types.append(ExerciseType(exercise_code=key, exercise_name=fake_exercise_types_data[key]))

        return ExerciseTypes(common_code=COMMON_CODE_EXERCISE_TYPE, items=exercise_types)


    # 게시물 등록
    def create_exercise_post(self, exercise_code: str, photos: list[PhotoFileInfo]) -> str:
        new_post = Post(
            post_id=create_post_id(),
            exercise_code=exercise_code,
            photos=photos
        )

        fake_exercise_posts_data[new_post.post_id] = new_post

        return new_post.post_id


    # 운동 목록 가져오기 (데이터베이스를 사용하면 쉽게 구현 가능)
    def get_exercise_posts(self, sort_comment_time: bool = False, order_desc: bool = True, filter_exercise_codes: list[str] = None) -> Posts:
        #Todo 아래 코드는 디버그 용도로 제거 요망
        # for key, value in fake_exercise_posts_data.items():
        #     print(key, ": ", value)

        # 운동 유형 필터 적용
        filtered_posts = fake_exercise_posts_data.copy()
        if filter_exercise_codes != None:
            for key, value in fake_exercise_posts_data.items():
                if value.exercise_code in filter_exercise_codes:
                    del filtered_posts[key]
        
        sorted_posts = []
        # 정렬 적용(기본: 내림차순)
        if sort_comment_time == True:   # 댓글로 정렬
            temp_comments = {}
            temp_no_comments = {}
            for post in filtered_posts.values():
                if len(post.comments) > 0:
                    post.comments.sort(key=operator.attrgetter('updated_time'), reverse=order_desc)
                    temp_comments[post.post_id] = post.comments[0].updated_time
                else:
                    temp_no_comments[post.post_id] = post.updated_time
            
            # 댓글 업데이트 일자로 정렬
            sorted_comments_post_id = sorted(temp_comments.items(), key=operator.itemgetter(1), reverse=order_desc)
            for post_id in sorted_comments_post_id:
                sorted_posts.append(filtered_posts[post_id[0]])
            
            # 댓글이 없는 경우의 처리
            for key in temp_no_comments.keys():
                sorted_posts.append(filtered_posts[key])

        else:   # (기본) 게시물로 정렬
            sorted_posts = sorted(filtered_posts.values(), key=operator.attrgetter('updated_time'), reverse=order_desc)

        return Posts(count=len(sorted_posts), items=sorted_posts)
    

    # 운동 게시물 가져오기
    def get_exercise_post(self, post_id) -> Post:
        if post_id in fake_exercise_posts_data:
            return fake_exercise_posts_data.get(post_id)
        else:
            return None
        

    # 운동 게시물(이전/다음 포함용) 가져오기
    def get_exercise_post_out(self, post_id) -> PostOut:
        sorted_posts = sorted(fake_exercise_posts_data.values(), key=operator.attrgetter('updated_time'))
        post_list_index = None
        for index, post in enumerate(sorted_posts):
            if post.post_id == post_id:
                post_list_index = index
                break

        p_post_id = ""
        n_post_id = ""
        if post_list_index - 1 >= 0:
            p_post_id = sorted_posts[post_list_index - 1].post_id

        if post_list_index + 1 < len(sorted_posts):
            n_post_id = sorted_posts[post_list_index + 1].post_id

        result = PostOut(
            created_time=sorted_posts[post_list_index].created_time,
            updated_time=sorted_posts[post_list_index].updated_time,
            post_id=sorted_posts[post_list_index].post_id,
            exercise_code=sorted_posts[post_list_index].exercise_code,
            photos=sorted_posts[post_list_index].photos,
            comments=sorted_posts[post_list_index].comments,
            prev_post_id=p_post_id,
            next_post_id=n_post_id
        )

        return result
        

    # 댓글 등록
    def create_comment(self, post_id: str, comment: CommentBase) -> str:
        new_comment_id = create_comment_id(post_id)
        
        fake_exercise_posts_data[post_id].comments.append(
            Comment(
                post_id=post_id,
                comment_id=new_comment_id,
                content=comment.content
            )
        )

        return new_comment_id
    

    # 게시물 삭제
    def delete_exercise_post(self, post_id: str):
        if post_id in fake_exercise_posts_data.keys():
            fake_exercise_posts_data.pop(post_id)
