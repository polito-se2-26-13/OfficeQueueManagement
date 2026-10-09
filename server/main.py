# run with: py -m uvicorn server.main:app --reload  (from project root)
from fastapi import FastAPI

from server.database import Base, engine, SessionLocal
from server.routes import counter_router, service_router, ticket_router

# create all tables on startup if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Office Queue Management")


@app.on_event("startup")
def seed_database():
    """Seed the database with sample data if it is empty."""
    from server.models.DAO.service_dao import ServiceDAO
    from server.models.DAO.counter_dao import CounterDAO
    from server.models.DAO.counter_service_dao import CouterServiceDAO

    db = SessionLocal()
    try:
        if db.query(ServiceDAO).count() == 0:
            services = [
                ServiceDAO(name="Customer Support", description="Assistance with customer requests and issues."),
                ServiceDAO(name="Payments",         description="Processing payments and transactions."),
                ServiceDAO(name="Document Collection", description="Collection of requested documents."),
                ServiceDAO(name="Technical Support",   description="Help with technical problems."),
            ]
            db.add_all(services)
            db.flush()   # populate service_id before using them in counter_services

        if db.query(CounterDAO).count() == 0:
            counters = [
                CounterDAO(position=3),
                CounterDAO(position=1),
                CounterDAO(position=4),
                CounterDAO(position=2),
            ]
            db.add_all(counters)
            db.flush()   # populate counter_id

            # wire up counter_services: each counter handles all services
            services = db.query(ServiceDAO).all()
            for counter in counters:
                for service in services:
                    db.add(CouterServiceDAO(
                        counter_id=counter.counter_id,
                        service_id=service.service_id,
                    ))

        db.commit()
    finally:
        db.close()


@app.get("/api/health")
def health():
    """Quick check that the backend is running."""
    return {"status": "ok"}


app.include_router(counter_router.router)
app.include_router(service_router.router)
app.include_router(ticket_router.router)
