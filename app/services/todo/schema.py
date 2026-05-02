from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BaseResponse(BaseModel):
    detail: str

class ErrorResponse(BaseResponse):
    pass

class Todo(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    done: bool
    created_at: datetime

class CreateTodoRequest(BaseModel):
    name: str
    description: Optional[str] = None

class CreateTodoResponse(Todo):
    pass

class UpdateTodoRequest(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None

class UpdateTodoResponse(Todo):
    pass

class UpdateTodoNotFoundResponse(BaseResponse):
    pass

class DeleteTodoRequest(BaseModel):
    id: int

class DeleteTodoResponse(BaseResponse):
    pass

class DeleteTodoNotFoundResponse(BaseResponse):
    pass

class GetTodoNotFoundResponse(BaseResponse):
    pass
