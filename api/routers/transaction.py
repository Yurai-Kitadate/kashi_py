from typing import List
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import api.cruds.transaction as transaction_crud
from api.db import get_db
import api.schemas.transaction as transaction_schema

router = APIRouter()

@router.post("/create/transaction", response_model=transaction_schema.ReturnedTransaction)
async def create_transaction(
    task_body: transaction_schema.InsertedTransaction, db: AsyncSession = Depends(get_db)
):
    return await transaction_crud.create_transaction(db, task_body)

@router.put("/done/{transaction_id}", response_model=transaction_schema.ReturnedTransaction)
async def done_transaction(
    transaction_id: int, task_body: transaction_schema.InsertedTransaction, db: AsyncSession = Depends(get_db)
):
    transaction = await transaction_crud.get_transaction(db, transaction_id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="transaction not found")

    return await transaction_crud.done_transaction(db, task_body, original=transaction)