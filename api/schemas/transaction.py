from pydantic import BaseModel

class InsertedTransaction(BaseModel):
    borrower_id       : int
    lender_id       : int
    yen            : int
    description    : str
    is_done         : int
    is_accepted     : int
    
class ReturnedTransaction(BaseModel):
    transaction_id  : int
    borrower_id       : int
    lender_id       : int
    yen            : int
    description    : str
    is_done         : int
    is_accepted     : int
    class Config:
      orm_mode = True
    
class RequestedTransaction(BaseModel):
    transaction_id  : int