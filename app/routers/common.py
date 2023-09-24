from typing import Annotated
from fastapi import APIRouter, Depends

from app.db import db_instance
from app.dependencies import get_current_user
from app.models.common import ExerciseTypes
from app.models.users import User


router = APIRouter(
    prefix="/common"
)


# 운동 유형 공통코드 제공
@router.get("/exercise-types", response_model=ExerciseTypes)
async def get_exercise_types(
    current_user: Annotated[User, Depends(get_current_user)]
) -> ExerciseTypes:
    return db_instance.get_exercise_types()