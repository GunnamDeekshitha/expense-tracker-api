import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas, database, auth
from ..utils.currency import convert_currency

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=schemas.ExpenseResponse)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    return crud.create_expense(db, expense, current_user.id)

@router.get("/", response_model=List[schemas.ExpenseResponse])
def read_expenses(
    category: Optional[str] = Query(None),
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None),
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.get_current_user)
):
    return crud.get_expenses(db, current_user.id, category, month, year)

@router.get("/{expense_id}", response_model=schemas.ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    exp = crud.get_expense(db, expense_id, current_user.id)
    if not exp:
        raise HTTPException(status_code=404, detail="Expense not found")
    return exp

@router.put("/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(expense_id: int, updates: schemas.ExpenseCreate, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    updated = crud.update_expense(db, expense_id, current_user.id, updates.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    ok = crud.delete_expense(db, expense_id, current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"detail": "Deleted"}

@router.get("/convert/{expense_id}")
def convert_expense_amount(
    expense_id: int,
    target_currency: str = "USD",
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.get_current_user)
):
    exp = crud.get_expense(db, expense_id, current_user.id)
    if not exp:
        raise HTTPException(status_code=404, detail="Expense not found")

    converted = convert_currency(exp.amount, exp.currency or "INR", target_currency)

    return {
        "original": exp.amount,
        "original_currency": exp.currency or "INR",
        "converted": converted,
        "target_currency": target_currency.upper()
    }
