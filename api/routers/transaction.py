from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import api.cruds.transaction as transaction_crud
from api.db import get_db
import api.schemas.transaction as transaction_schema

router = APIRouter()


@router.post("/create/transaction", response_model=transaction_schema.ReturnedTransaction)
async def create_transaction(
    transaction_body: transaction_schema.InsertedTransaction, db: AsyncSession = Depends(get_db)
):
    return await transaction_crud.create_transaction(db, transaction_body)


@router.put("/done/{transaction_id}", response_model=transaction_schema.ReturnedTransaction)
async def done_transaction(
    transaction_id: int, transaction_body: transaction_schema.InsertedTransaction, db: AsyncSession = Depends(get_db)
):
    transaction = await transaction_crud.get_transaction(db, transaction_id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="transaction not found")

    return await transaction_crud.done_transaction(db, transaction_body, original=transaction)


@router.put("/accept/{transaction_id}", response_model=transaction_schema.ReturnedTransaction)
async def done_transaction(
    transaction_id: int, transaction_body: transaction_schema.InsertedTransaction, db: AsyncSession = Depends(get_db)
):
    transaction = await transaction_crud.get_transaction(db, transaction_id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="transaction not found")

    return await transaction_crud.accept_transaction(db, transaction_body, original=transaction)


@router.put("/validate/{transaction_id}", response_model=transaction_schema.ReturnedTransaction)
async def validate_transaction(
    transaction_id: int, transaction_body: transaction_schema.InsertedTransaction, db: AsyncSession = Depends(get_db)
):
    transaction = await transaction_crud.get_transaction(db, transaction_id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="transaction not found")

    return await transaction_crud.validate_transaction(db, transaction_body, original=transaction)


@router.get("/get/transactions", response_model=List[transaction_schema.ReturnedTransaction])
async def get_transactions(db: AsyncSession = Depends(get_db)):
    return await transaction_crud.get_transactions(db)


@router.delete("/delete/transaction/{transaction_id}", response_model=None)
async def delete_user(transaction_id: int, db: AsyncSession = Depends(get_db)):
    transaction = await transaction_crud.get_transaction(db, transaction_id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="transaction not found")

    return await transaction_crud.delete_transaction(db, original=transaction)


@router.get("/get/transactions/borrow/{borrower_id}", response_model=List[transaction_schema.ReturnedTransaction])
async def get_borrow_transactions(borrower_id: int, db: AsyncSession = Depends(get_db)):
    return await transaction_crud.get_borrow_transactions(db, borrower_id=borrower_id)


@router.get("/get/transactions/lend/{lender_id}", response_model=List[transaction_schema.ReturnedTransaction])
async def get_lender_transactions(lender_id: int, db: AsyncSession = Depends(get_db)):
    return await transaction_crud.get_lend_transactions(db, lender_id=lender_id)


@router.get("/get/transactions/both/{user_id}", response_model=List[transaction_schema.ReturnedTransaction])
async def get_both_transactions(user_id: int, db: AsyncSession = Depends(get_db)):
    return await transaction_crud.get_both_transactions(db, user_id=user_id)
