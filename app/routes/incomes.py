from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas, database, auth
from ..utils.currency import convert_currency

router = APIRouter(prefix="/incomes", tags=["Incomes"])

@router.post("/", response_model=schemas.IncomeResponse)
def create_income(income: schemas.IncomeCreate, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    return crud.create_income(db, income, current_user.id)

@router.get("/", response_model=List[schemas.IncomeResponse])
def read_incomes(
    source: Optional[str] = Query(None),
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None),
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.get_current_user)
):
    return crud.get_incomes(db, current_user.id, source, month, year)

@router.get("/{income_id}", response_model=schemas.IncomeResponse)
def get_income(income_id: int, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    inc = crud.get_income(db, income_id, current_user.id)
    if not inc:
        raise HTTPException(status_code=404, detail="Income not found")
    return inc

@router.put("/{income_id}", response_model=schemas.IncomeResponse)
def update_income(income_id: int, updates: schemas.IncomeCreate, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    updated = crud.update_income(db, income_id, current_user.id, updates.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Income not found")
    return updated

@router.delete("/{income_id}")
def delete_income(income_id: int, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    ok = crud.delete_income(db, income_id, current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Income not found")
    return {"detail": "Deleted"}

from ..utils.currency import convert_currency

@router.get("/convert/{income_id}")
def convert_income_amount(
    income_id: int,
    target_currency: str = "USD",
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.get_current_user)
):
    inc = crud.get_income(db, income_id, current_user.id)
    if not inc:
        raise HTTPException(status_code=404, detail="Income not found")

    converted = convert_currency(inc.amount, inc.currency or "INR", target_currency)

    return {
        "original": inc.amount,
        "original_currency": inc.currency or "INR",
        "converted": converted,
        "target_currency": target_currency.upper()
    }

