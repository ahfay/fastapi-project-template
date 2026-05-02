from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, Params

from depends.db import get_session
from services.todo.service import TodoService
from services.todo.schema import *

router = APIRouter(
    prefix="/v1/api/todo",
    tags=["Todo"]
)

@router.post("/", 
             response_model=CreateTodoResponse,
             status_code=201,
             responses={
                500: {"model": ErrorResponse, "description": "Internal Server Error"},
             })
async def create_todo(new_todo: CreateTodoRequest, db: AsyncSession = Depends(get_session)):
    todo_service = TodoService(db)
    return await todo_service.create_todo(new_todo)

@router.get("/", 
            response_model=Page[Todo],
            status_code=200,
            responses={
                404: {"model": GetTodoNotFoundResponse, "description": "Todo not found"},
                500: {"model": ErrorResponse, "description": "Internal Server Error"}
            })
async def get_todos(done: bool = False, params: Params = Depends(), db: AsyncSession = Depends(get_session)):
    todo_service = TodoService(db)
    return await todo_service.get_todos(params, done)

@router.put("/", 
            response_model=UpdateTodoResponse,
            status_code=200,
            responses={
                404: {"model": UpdateTodoNotFoundResponse, "description": "Todo not found"},
                500: {"model": ErrorResponse, "description": "Internal Server Error"}
            })
async def update_todo(update_todo: UpdateTodoRequest, db: AsyncSession = Depends(get_session)):
    todo_service = TodoService(db)
    return await todo_service.update_todo(update_todo)

@router.delete("/", 
               response_model=DeleteTodoResponse,
               status_code=200,
               responses={
                   404: {"model": DeleteTodoNotFoundResponse, "description": "Todo not found"},
                   500: {"model": ErrorResponse, "description": "Internal Server Error"}
               })
async def delete_todo(todo: DeleteTodoRequest, db: AsyncSession = Depends(get_session)):
    todo_service = TodoService(db)
    return await todo_service.delete_todo(todo)