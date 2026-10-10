# run with: py -m uvicorn server.main:app --reload  (from project root)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.config.config import ORIGIN
from server.database import Base, engine, SessionLocal
from server.routes import counter_router, service_router, ticket_router

# create all tables on startup if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Office Queue Management")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGIN,
    allow_credentials=True, #do we need it?
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    """Quick check that the backend is running."""
    return {"status": "ok"}


app.include_router(counter_router.router)
app.include_router(service_router.router)
app.include_router(ticket_router.router)
