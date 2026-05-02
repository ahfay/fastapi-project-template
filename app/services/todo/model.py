from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

from config import settings


class TodoSchemaTable(SQLModel, table=True):
    __tablename__ = "todo_table"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = Field(default=None)
    done: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(settings.TIMEZONE))