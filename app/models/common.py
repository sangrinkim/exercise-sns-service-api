from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field


# 공통코드 정의
COMMON_CODE_EXERCISE_TYPE = "exercise_type"  # 운동 유형


class Common(BaseModel):
    common_code: str


class ExerciseType(BaseModel):
    exercise_code: str
    exercise_name: str


class ExerciseTypes(Common):
    items: list[ExerciseType]


class ModifiyDateTime(BaseModel):
    created_time: datetime = Field(default_factory=datetime.now)
    updated_time: datetime = Field(default_factory=datetime.now)