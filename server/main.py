"""Entry point of the backend. Start it from this folder with: uvicorn main:app --reload"""
from fastapi import FastAPI

from server.database import Base, engine
from server.routes import (counter_router)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Office Queue Management")


@app.get("/api/health")
def health():
    """Quick check that the backend is running."""
    return {"status": "ok"}


app.include_router(counter_router.router)
