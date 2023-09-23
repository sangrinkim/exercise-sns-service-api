from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return { "message": "EXERCISE_SNS_SERVICE_API" }