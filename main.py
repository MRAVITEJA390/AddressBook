from fastapi import FastAPI

app = FastAPI()


@app.get('/health_check/')
async def hello_world():
    return {"message": "Hello World"}
