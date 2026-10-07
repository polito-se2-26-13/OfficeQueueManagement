"""Entry point of the backend. Start it from this folder with: uvicorn main:app --reload"""
from fastapi import FastAPI

import models  # noqa: F401  imported so that its tables exist before create_all
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Office Queue Management")


@app.get("/api/health")
def health():
    """Quick check that the backend is running."""
    return {"status": "ok"}
