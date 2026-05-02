from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
import logging

logger = logging.getLogger("services.todo.service")
from .model import *
from .schema import *

class TodoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_todo(self, new_todo: CreateTodoRequest):
        try:
            todo = TodoSchemaTable(
                name=new_todo.name,
                description=new_todo.description
            )
            self.db.add(todo)
            await self.db.commit()
            await self.db.refresh(todo)
            return JSONResponse(
                status_code=201,
                content=jsonable_encoder(CreateTodoResponse(**todo.model_dump()).model_dump())
            )
        except Exception as e:
            logger.error(f"Todo creation failed: {e}")
            raise HTTPException(status_code=500, detail="Todo creation failed")


    async def get_todos(self, params: Params, done: bool = False):
        try:
            query = select(TodoSchemaTable).where(TodoSchemaTable.done == done)
            result = await self.db.execute(query)
            todos = result.all()
            if not todos:
                return JSONResponse(
                    status_code=404,
                    content=GetTodoNotFoundResponse(detail="Todo not found").model_dump()
                )
            return await paginate(self.db, query, params)
        except Exception as e:
            logger.error(f"Todo retrieval failed: {e}")
            raise HTTPException(status_code=500, detail="Todo retrieval failed")

    async def update_todo(self, update_todo: UpdateTodoRequest):
        try:
            query = select(TodoSchemaTable).where(TodoSchemaTable.id == update_todo.id)
            result = await self.db.execute(query)
            todo = result.scalar_one_or_none()
            if not todo:
                return JSONResponse(
                    status_code=404,
                    content=UpdateTodoNotFoundResponse(detail="Todo not found").model_dump()
                )
            todo.name = update_todo.name if update_todo.name else todo.name
            todo.description = update_todo.description if update_todo.description else todo.description
            todo.done = update_todo.done if update_todo.done is not None else todo.done
            await self.db.commit()
            await self.db.refresh(todo)
            return JSONResponse(
                status_code=200,
                content=jsonable_encoder(UpdateTodoResponse(**todo.model_dump()).model_dump())
            )
        except Exception as e:
            logger.error(f"Todo update failed: {e}")
            raise HTTPException(status_code=500, detail="Todo update failed")
    
    async def delete_todo(self, todo: DeleteTodoRequest):
        try:
            query = select(TodoSchemaTable).where(TodoSchemaTable.id == todo.id)
            result = await self.db.execute(query)
            todo = result.scalar_one_or_none()
            if not todo:
                return JSONResponse(
                    status_code=404,
                    content=DeleteTodoNotFoundResponse(detail="Todo not found").model_dump()
                )
            await self.db.delete(todo)
            await self.db.commit()
            return JSONResponse(
                status_code=200,
                content=DeleteTodoResponse(detail="Todo deleted").model_dump()
            )
        except Exception as e:
            logger.error(f"Todo deletion failed: {e}")
            raise HTTPException(status_code=500, detail="Todo deletion failed")