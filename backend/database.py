from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os 

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Agar postgres:// aaye toh postgresql:// me convert
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Cloud PostgreSQL connection engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Connection drop hone se bachayega
    pool_recycle=300
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()