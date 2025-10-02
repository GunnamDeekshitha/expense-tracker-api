# app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# --- User ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

# --- Expense ---
class ExpenseBase(BaseModel):
    description: Optional[str] = None
    amount: float
    category: Optional[str] = None
    currency: Optional[str] = "INR"
    date: Optional[datetime] = None

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True

# --- Income ---
class IncomeBase(BaseModel):
    description: Optional[str] = None
    amount: float
    source: Optional[str] = None
    currency: Optional[str] = "INR"
    date: Optional[datetime] = None

class IncomeCreate(IncomeBase):
    pass

class IncomeResponse(IncomeBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True

# --- Monthly analytics ---
class MonthlyAnalyticsItem(BaseModel):
    month: int
    total_income: float
    total_expense: float
    net: float

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
