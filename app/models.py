# app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    expenses = relationship("Expense", back_populates="owner", cascade="all,delete-orphan")
    incomes = relationship("Income", back_populates="owner", cascade="all,delete-orphan")


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255))
    amount = Column(Float, nullable=False)
    category = Column(String(50))
    currency = Column(String(10), default="INR")
    date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    owner = relationship("User", back_populates="expenses")


class Income(Base):
    __tablename__ = "incomes"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255))
    amount = Column(Float, nullable=False)
    source = Column(String(100))
    currency = Column(String(10), default="INR")
    date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    owner = relationship("User", back_populates="incomes")
