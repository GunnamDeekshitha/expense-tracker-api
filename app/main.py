# app/main.py
from fastapi import FastAPI
from .database import engine, Base
from .routes import users, expenses, incomes
from fastapi.middleware.cors import CORSMiddleware

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(expenses.router)
app.include_router(incomes.router)


# Combined analytics endpoint
from fastapi import Depends
from sqlalchemy.orm import Session
from . import crud, database, schemas, auth

@app.get("/analytics/{year}", response_model=list[schemas.MonthlyAnalyticsItem], tags=["Analytics"])
def analytics(year: int, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    return crud.get_monthly_analytics(db, current_user.id, year)
