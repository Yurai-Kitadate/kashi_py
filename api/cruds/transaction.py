from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Optional
import api.models.transaction as transaction_model
import api.schemas.transaction as transaction_schema
from sqlalchemy import select


async def create_transaction(
    db: AsyncSession, task_create: transaction_schema.InsertedTransaction
) -> transaction_model.Transaction:
    task = transaction_model.Transaction(**task_create.dict())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_transaction(db: AsyncSession, transaction_id: int) -> Optional[transaction_model.Transaction]:
    result: Result = await db.execute(
        select(transaction_model.Transaction).filter(transaction_model.Transaction.transaction_id == transaction_id)
    )
    transaction: Optional[Tuple[transaction_model.Transaction]] = result.first()
    return transaction[0] if transaction is not None else None 


async def done_transaction(
    db: AsyncSession, transaction_create: transaction_schema.RequestedTransaction, original: transaction_model.Transaction
) -> transaction_model.Transaction:
    original.is_done = 1
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original