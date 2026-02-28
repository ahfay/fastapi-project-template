from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession 
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings
from models.dummy import DummyModel


engine = create_async_engine(settings.db_url, echo=False)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)