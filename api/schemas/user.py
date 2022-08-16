from pydantic import BaseModel

class InsertedUser(BaseModel):
    user_name       : str

class ReturnedUser(BaseModel):
    user_id         : int
    user_name       : str
    class Config:
      orm_mode = True

class RequestedUser(BaseModel):
    user_id         : int
