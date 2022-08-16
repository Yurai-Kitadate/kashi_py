from sqlalchemy.ext.asyncio import AsyncSession

import api.models.user as user_model
import api.schemas.user as user_schema


async def create_user(
    db: AsyncSession, task_create: user_schema.InsertedUser
) -> user_model.User:
    task = user_model.User(**task_create.dict())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task