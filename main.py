from fastapi import FastAPI
from apis import router

app = FastAPI()


@app.get('/health_check/')
async def hello_world():
    return {"message": "Hello World"}


app.include_router(router)
