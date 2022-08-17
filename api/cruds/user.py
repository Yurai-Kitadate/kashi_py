from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Optional
import api.models.user as user_model
import api.schemas.user as user_schema
from sqlalchemy import select

async def create_user(
    db: AsyncSession, created_user: user_schema.InsertedUser
) -> user_model.User:
    user = user_model.User(**created_user.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_users(db: AsyncSession) -> List[Tuple[int,str]]:
    result: Result = await (
        db.execute(
            select(
                user_model.User.user_id,
                user_model.User.user_name,
            )
        )
    )
    return result.all()
