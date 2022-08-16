from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import api.cruds.user as user_crud
from api.db import get_db
import api.schemas.user as user_schema

router = APIRouter()

@router.post("/create/user", response_model=user_schema.ReturnedUser)
async def create_user(
    task_body: user_schema.InsertedUser, db: AsyncSession = Depends(get_db)
):
    return await user_crud.create_user(db, task_body)