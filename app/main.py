from fastapi import Depends, FastAPI

from .routers import common, posts, users


app = FastAPI()


app.include_router(users.router)
app.include_router(common.router)
app.include_router(posts.router)


# 테스트 용도(핑)
# @app.get("/")
# async def root():
#     return { "message": "EXERCISE_SNS_SERVICE_API" }