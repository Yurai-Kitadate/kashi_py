from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Optional
import api.models.transaction as transaction_model
import api.schemas.transaction as transaction_schema
from sqlalchemy import select


async def create_transaction(
    db: AsyncSession, created_transaction: transaction_schema.InsertedTransaction
) -> transaction_model.Transaction:
    transaction = transaction_model.Transaction(**created_transaction.dict())
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction

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

async def accept_transaction(
    db: AsyncSession, transaction_create: transaction_schema.RequestedTransaction, original: transaction_model.Transaction
) -> transaction_model.Transaction:
    original.is_accepted = 1
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def get_transactions(db: AsyncSession) -> List[Tuple[int, int,int,int,str,int,int]]:
    result: Result = await (
        db.execute(
            select(
                transaction_model.Transaction.transaction_id,
                transaction_model.Transaction.renter_id,
                transaction_model.Transaction.lender_id,
                transaction_model.Transaction.yen,
                transaction_model.Transaction.description,
                transaction_model.Transaction.is_done,
                transaction_model.Transaction.is_accepted
            )
        )
    )
    return result.all()

