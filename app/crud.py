from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from typing import List, Dict

from . import models, schemas, auth

def create_user(db: Session, user_in: schemas.UserCreate):
    hashed = auth.hash_password(user_in.password)
    db_user = models.User(username=user_in.username, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_expense(db: Session, expense_in: schemas.ExpenseCreate, user_id: int):
    payload = expense_in.dict()
    if payload.get("date") is None:
        payload["date"] = datetime.utcnow()
    db_exp = models.Expense(**payload, user_id=user_id)
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp

def get_expense(db: Session, expense_id: int, user_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == user_id).first()

def update_expense(db: Session, expense_id: int, user_id: int, updates: dict):
    exp = get_expense(db, expense_id, user_id)
    if not exp:
        return None
    for k, v in updates.items():
        if hasattr(exp, k) and v is not None:
            setattr(exp, k, v)
    db.commit()
    db.refresh(exp)
    return exp

def delete_expense(db: Session, expense_id: int, user_id: int):
    exp = get_expense(db, expense_id, user_id)
    if not exp:
        return False
    db.delete(exp)
    db.commit()
    return True

def get_expenses(db: Session, user_id: int, category: str = None, month: int = None, year: int = None):
    query = db.query(models.Expense).filter(models.Expense.user_id == user_id)
    if category:
        query = query.filter(models.Expense.category == category)
    if month:
        query = query.filter(extract("month", models.Expense.date) == month)
    if year:
        query = query.filter(extract("year", models.Expense.date) == year)
    return query.order_by(models.Expense.date.desc()).all()

def create_income(db: Session, income_in: schemas.IncomeCreate, user_id: int):
    payload = income_in.dict()
    if payload.get("date") is None:
        payload["date"] = datetime.utcnow()
    db_inc = models.Income(**payload, user_id=user_id)
    db.add(db_inc)
    db.commit()
    db.refresh(db_inc)
    return db_inc

def get_income(db: Session, income_id: int, user_id: int):
    return db.query(models.Income).filter(models.Income.id == income_id, models.Income.user_id == user_id).first()

def update_income(db: Session, income_id: int, user_id: int, updates: dict):
    inc = get_income(db, income_id, user_id)
    if not inc:
        return None
    for k, v in updates.items():
        if hasattr(inc, k) and v is not None:
            setattr(inc, k, v)
    db.commit()
    db.refresh(inc)
    return inc

def delete_income(db: Session, income_id: int, user_id: int):
    inc = get_income(db, income_id, user_id)
    if not inc:
        return False
    db.delete(inc)
    db.commit()
    return True

def get_incomes(db: Session, user_id: int, source: str = None, month: int = None, year: int = None):
    query = db.query(models.Income).filter(models.Income.user_id == user_id)
    if source:
        query = query.filter(models.Income.source == source)
    if month:
        query = query.filter(extract("month", models.Income.date) == month)
    if year:
        query = query.filter(extract("year", models.Income.date) == year)
    return query.order_by(models.Income.date.desc()).all()

def get_monthly_analytics(db: Session, user_id: int, year: int):
    incomes = (
        db.query(extract("month", models.Income.date).label("m"), func.coalesce(func.sum(models.Income.amount), 0).label("total"))
        .filter(models.Income.user_id == user_id, extract("year", models.Income.date) == year)
        .group_by(extract("month", models.Income.date))
        .all()
    )
    income_map = {int(row.m): float(row.total) for row in incomes}


    expenses = (
        db.query(extract("month", models.Expense.date).label("m"), func.coalesce(func.sum(models.Expense.amount), 0).label("total"))
        .filter(models.Expense.user_id == user_id, extract("year", models.Expense.date) == year)
        .group_by(extract("month", models.Expense.date))
        .all()
    )
    expense_map = {int(row.m): float(row.total) for row in expenses}
    analytics = []
    for m in range(1, 13):
        inc_total = income_map.get(m, 0.0)
        exp_total = expense_map.get(m, 0.0)
        analytics.append({
            "month": m,
            "total_income": inc_total,
            "total_expense": exp_total,
            "net": inc_total - exp_total
        })
    return analytics
