from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import logging

from config import settings
from db import create_db_and_tables
from core.logger import setup_logging

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

@app.get("/")
async def root():
    logger.info("Hello World")
    return {"message": "Hello World",
            "test_api": settings.test_api}

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=7777)

