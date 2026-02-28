from sqlmodel import SQLModel, Field

class DummyModel(SQLModel, table=True):
    __tablename__ = "dummy_table"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
