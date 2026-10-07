"""Database connection shared by the whole backend (SQLite file next to this module)."""
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = f"sqlite:///{Path(__file__).parent / 'queue.db'}"

# check_same_thread=False lets FastAPI use the connection from its worker threads
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """Parent class of every table defined in models.py."""


def get_db():
    """FastAPI dependency: gives each request its own session and closes it at the end."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
