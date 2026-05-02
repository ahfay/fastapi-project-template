from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import logging

from config import settings
from depends.db import create_db_and_tables
from core.logger import setup_logging
from routers.todo.v1 import router as todo_router

setup_logging()
logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_db_and_tables()
        yield
    except:
        pass

app = FastAPI(lifespan=lifespan)
app.include_router(todo_router)

@app.get("/")
async def root():
    logger.info("Hello World")
    return {"message": "Hello World",
            "test_api": settings.TEST_API}

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=7777)

