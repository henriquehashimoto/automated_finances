from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True)
    data = Column(DateTime, nullable=False)
    value_amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    category_group = Column(String)
    spender = Column(String)
    is_recurrent = Column(Boolean)
    installment_amounts = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())

