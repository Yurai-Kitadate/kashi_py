from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Optional
import api.models.transaction as transaction_model
import api.schemas.transaction as transaction_schema
from sqlalchemy import select, or_, and_
from sqlalchemy.engine import Result


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
        select(transaction_model.Transaction).filter(
            transaction_model.Transaction.transaction_id == transaction_id)
    )
    transaction: Optional[Tuple[transaction_model.Transaction]
                          ] = result.first()
    return transaction[0] if transaction is not None else None


async def delete_transaction(db: AsyncSession, original: transaction_model.Transaction) -> None:
    await db.delete(original)
    await db.commit()


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


async def validate_transaction(
    db: AsyncSession, transaction_create: transaction_schema.RequestedTransaction, original: transaction_model.Transaction
) -> transaction_model.Transaction:
    original.is_valid = 1
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def get_transactions(db: AsyncSession) -> List[Tuple[int, int, int, int, str, int, int]]:
    result: Result = await (
        db.execute(
            select(
                transaction_model.Transaction.transaction_id,
                transaction_model.Transaction.borrower_id,
                transaction_model.Transaction.lender_id,
                transaction_model.Transaction.applier_id,
                transaction_model.Transaction.yen,
                transaction_model.Transaction.description,
                transaction_model.Transaction.is_valid,
                transaction_model.Transaction.is_done,
                transaction_model.Transaction.is_accepted
            )
        )
    )
    return result.all()


async def delete_transaction(db: AsyncSession, original: transaction_model.Transaction) -> None:
    await db.delete(original)
    await db.commit()


async def get_borrow_transactions(db: AsyncSession, borrower_id: int) -> List[transaction_model.Transaction]:
    result: Result = await db.execute(
        select(
            transaction_model.Transaction.transaction_id,
            transaction_model.Transaction.borrower_id,
            transaction_model.Transaction.lender_id,
            transaction_model.Transaction.applier_id,
            transaction_model.Transaction.yen,
            transaction_model.Transaction.description,
            transaction_model.Transaction.is_valid,
            transaction_model.Transaction.is_done,
            transaction_model.Transaction.is_accepted
        ).filter(and_(transaction_model.Transaction.borrower_id == borrower_id, transaction_model.Transaction.is_valid == 1, transaction_model.Transaction.is_done == 0))
    )
    return result.all()


async def get_lend_transactions(db: AsyncSession, lender_id: int) -> List[transaction_model.Transaction]:
    result: Result = await db.execute(
        select(
            transaction_model.Transaction.transaction_id,
            transaction_model.Transaction.borrower_id,
            transaction_model.Transaction.lender_id,
            transaction_model.Transaction.applier_id,
            transaction_model.Transaction.yen,
            transaction_model.Transaction.description,
            transaction_model.Transaction.is_valid,
            transaction_model.Transaction.is_done,
            transaction_model.Transaction.is_accepted
        ).filter(and_(transaction_model.Transaction.lender_id == lender_id, transaction_model.Transaction.is_valid == 1, transaction_model.Transaction.is_done == 0))
    )
    return result.all()


async def get_both_transactions(db: AsyncSession, user_id: int) -> List[transaction_model.Transaction]:
    result: Result = await db.execute(
        select(
            transaction_model.Transaction.transaction_id,
            transaction_model.Transaction.borrower_id,
            transaction_model.Transaction.lender_id,
            transaction_model.Transaction.applier_id,
            transaction_model.Transaction.yen,
            transaction_model.Transaction.description,
            transaction_model.Transaction.is_valid,
            transaction_model.Transaction.is_done,
            transaction_model.Transaction.is_accepted
        ).filter(and_(or_(transaction_model.Transaction.lender_id == user_id, transaction_model.Transaction.borrower_id == user_id), transaction_model.Transaction.is_valid == 1), transaction_model.Transaction.is_done == 0)
    )
    return result.all()


async def get_applied_transactions(db: AsyncSession, user_id: int) -> List[transaction_model.Transaction]:
    result: Result = await db.execute(
        select(
            transaction_model.Transaction.transaction_id,
            transaction_model.Transaction.borrower_id,
            transaction_model.Transaction.lender_id,
            transaction_model.Transaction.applier_id,
            transaction_model.Transaction.yen,
            transaction_model.Transaction.description,
            transaction_model.Transaction.is_valid,
            transaction_model.Transaction.is_done,
            transaction_model.Transaction.is_accepted
        ).filter(
            and_(transaction_model.Transaction.is_accepted == 0,
                 or_(
                     and_(
                         or_(
                             transaction_model.Transaction.lender_id == user_id, transaction_model.Transaction.borrower_id == user_id), transaction_model.Transaction.is_valid == 0),
                     and_(transaction_model.Transaction.is_done == 1, transaction_model.Transaction.lender_id == user_id,))))
    )
    return result.all()


async def get_appling_transactions(db: AsyncSession, user_id: int) -> List[transaction_model.Transaction]:
    result: Result = await db.execute(
        select(
            transaction_model.Transaction.transaction_id,
            transaction_model.Transaction.borrower_id,
            transaction_model.Transaction.lender_id,
            transaction_model.Transaction.applier_id,
            transaction_model.Transaction.yen,
            transaction_model.Transaction.description,
            transaction_model.Transaction.is_valid,
            transaction_model.Transaction.is_done,
            transaction_model.Transaction.is_accepted
        ).filter(or_(and_(transaction_model.Transaction.applier_id == user_id, transaction_model.Transaction.is_valid == 0), transaction_model.Transaction.borrower_id == user_id, transaction_model.Transaction.is_done == 1))
    )
    return result.all()
