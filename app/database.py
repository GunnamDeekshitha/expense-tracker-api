from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USER = "root"
DB_PASS = "password"
DB_NAME = "expense_db"
DB_HOST = "localhost"
DB_PORT = 3306

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://root:replace-your-password@localhost:3306/expense_tracker"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
