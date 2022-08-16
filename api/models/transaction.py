from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base


class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True)
    renter_id = Column(Integer,nullable=False)
    lender_id = Column(Integer,nullable=False)
    yen       = Column(Integer,nullable=False)
    description = Column(String(1024))
    is_done     = Column(Integer,nullable=False)
    is_accepted = Column(Integer,nullable=False)