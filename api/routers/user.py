from typing import List
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import api.cruds.user as user_crud
from api.db import get_db
import api.schemas.user as user_schema

router = APIRouter()

@router.post("/create/user", response_model=user_schema.ReturnedUser)
async def create_user(
    user_body: user_schema.InsertedUser, db: AsyncSession = Depends(get_db)
):
    return await user_crud.create_user(db, user_body)

@router.get("/get/users", response_model=List[user_schema.ReturnedUser])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await user_crud.get_users(db)

@router.delete("/delete/user/{user_id}", response_model=None)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return await user_crud.delete_user(db, original=user)