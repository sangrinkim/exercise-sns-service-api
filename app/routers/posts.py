import os
import shutil
import time
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse

from app.config import (
    UPLOAD_PHOTO_FILE_DIR, 
    VALID_PHOTO_EXTENTIONS, 
    MAX_NUMBER_UPLOAD_PHOTO,
    SAVE_PHOTO_FILE_TIME_FORMAT
)
from app.db import db_instance
from app.dependencies import get_current_user, get_current_user_permission
from app.models.posts import CommentBase, PhotoFileInfo, Post, PostOut, Posts
from app.models.users import User


router = APIRouter(
    prefix="/posts"
)


# 사진 폴더 확인 및 생성
os.makedirs(UPLOAD_PHOTO_FILE_DIR, exist_ok=True)


# 운동 목록 가져오기
@router.get("", response_model=Posts)
async def get_post_list(
    current_user: Annotated[User, Depends(get_current_user)],
    sort_comment_time: bool = False, 
    order_desc: bool = True, 
    filter_exercise_codes: list[str] = Query(None)
) -> any:
    # Todo: 목록의 개수 제한이 없다. -> 페이징 처리가 필요

    return db_instance.get_exercise_posts(sort_comment_time, order_desc, filter_exercise_codes)


# 운동 게시물 등록
@router.post("")
async def create_post(
    current_user: Annotated[User, Depends(get_current_user)],
    exercise_code: str, 
    files: list[UploadFile] = File(...)) -> JSONResponse:
    # 파일 등록 개수 제한
    if len(files) > MAX_NUMBER_UPLOAD_PHOTO:
        # Todo: 예외 핸들링 필요 -> 한 곳에 모아서 처리하는 것이 좋음
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="사진은 최대 5장까지 업로드 가능합니다.")

    # 이미지 파일 확장자 제한
    for file in files:
        if not file.filename.endswith(VALID_PHOTO_EXTENTIONS):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="사진(이미지) 파일만 업로드 할 수 있습니다.")

    # 업로드 파일 저장 및 정보 생성
    try:
        photo_list = []
        save_file_time = time.strftime(SAVE_PHOTO_FILE_TIME_FORMAT)
        for index, photo in enumerate(files):
            save_file_name = save_file_time + "_" + photo.filename.replace(" ", "-")

            with open(os.path.join(UPLOAD_PHOTO_FILE_DIR, save_file_name), "wb") as buffer:
                shutil.copyfileobj(photo.file, buffer)

            photo_list.append(PhotoFileInfo(file_no=index + 1, original_file_name=photo.filename, save_file_name=save_file_name))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    # 게시물 정보 DB에 저장
    post_id = db_instance.create_exercise_post(exercise_code=exercise_code, photos=photo_list)

    return JSONResponse(content={"post_id": post_id}, status_code=201)


# 댓글 등록
@router.post("/{post_id}/comments")
async def create_comment(
    current_user: Annotated[User, Depends(get_current_user)],
    post_id: str, comment: CommentBase) -> JSONResponse:
    post = db_instance.get_exercise_post(post_id)
    if post == None:
        raise HTTPException(status_code=400, detail="해당 게시물을 찾을 수 없습니다.")

    comment_id = db_instance.create_comment(post_id, comment)

    return JSONResponse(content={"comment_id": comment_id}, status_code=201)


# 운동 게시물 정보 가져오기
@router.get("/{post_id}")
async def get_post(
    current_user: Annotated[User, Depends(get_current_user)],
    post_id: str) -> PostOut:
    post = db_instance.get_exercise_post(post_id)
    if post == None:
        raise HTTPException(status_code=204, detail="해당 게시물을 찾을 수 없습니다.")
    
    result = db_instance.get_exercise_post_out(post_id)

    return result


# 운동 사진 가져오기
@router.get("/{post_id}/photos/{file_no}")
async def get_post(
    current_user: Annotated[User, Depends(get_current_user)],
    post_id: str, file_no: int) -> Post:
    post = db_instance.get_exercise_post(post_id)
    if post == None:
        raise HTTPException(status_code=204, detail="해당 게시물을 찾을 수 없습니다.")

    photoFileInfo = None
    for p in post.photos:
        if p.file_no == file_no:
            photoFileInfo = p

    if photoFileInfo == None:
        raise HTTPException(status_code=204, detail="해당 사진은 찾을 수 없습니다.")

    file_path = os.path.join(UPLOAD_PHOTO_FILE_DIR, photoFileInfo.save_file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=204, detail="해당 사진은 찾을 수 없습니다.")

    return FileResponse(file_path, filename=photoFileInfo.original_file_name)


# 운동 게시물 삭제
@router.delete("/{post_id}")
async def delete_post(
    current_user: Annotated[User, Depends(get_current_user_permission)],
    post_id: str):
    # Todo 파일 삭제
    # post = db_instance.get_exercise_post(post_id)
    # if post != None:
    #     pass

    # 게시물 정보 삭제
    db_instance.delete_exercise_post(post_id)

    return {"message": post_id + "가 삭제되었습니다."}