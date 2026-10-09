# run with: py -3.10 -m uvicorn main:app --reload
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models.DAO.models import ServiceDAO, TicketDAO
from models.DTO.schemas import (
    ServiceDTO, ServicesResponseDTO,
    TicketRequestDTO, TicketResponseDTO,
    NextCustomerRequestDTO, NextCustomerResponseDTO
)

# make sure tables exist before anything starts
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Office Queue Management")

@app.on_event("startup")
def startup_event():
    # add some default services if db is empty
    db = next(get_db())
    if db.query(ServiceDAO).count() == 0:
        db.add_all([
            ServiceDAO(name="Shipping", description="Send packages and letters", prefix="S"),
            ServiceDAO(name="Accounts", description="Manage your bank account", prefix="A"),
        ])
        db.commit()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/services", response_model=ServicesResponseDTO)
def get_services(db: Session = Depends(get_db)):
    services = db.query(ServiceDAO).all()
    # map each db row to a DTO
    services_dto = [
        ServiceDTO(
            service_id=s.id,
            service_name=s.name,
            description=s.description
        ) for s in services
    ]
    return {"services": services_dto}


@app.post("/api/ticket", response_model=TicketResponseDTO)
def create_ticket(request: TicketRequestDTO, db: Session = Depends(get_db)):
    service = db.query(ServiceDAO).filter(ServiceDAO.id == request.service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    # ticket code is just prefix + how many tickets already exist for this service
    ticket_count = db.query(TicketDAO).filter(TicketDAO.service_id == service.id).count()
    ticket_code = f"{service.prefix}{ticket_count + 1:03d}"

    new_ticket = TicketDAO(
        code=ticket_code,
        service_id=service.id,
        status="waiting"
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return TicketResponseDTO(
        ticket_id=new_ticket.id,
        ticket_code=new_ticket.code
    )


@app.put("/api/customers/next", response_model=NextCustomerResponseDTO)
def call_next_customer(request: NextCustomerRequestDTO, db: Session = Depends(get_db)):
    # grab the oldest waiting ticket
    next_ticket = db.query(TicketDAO).filter(TicketDAO.status == "waiting").order_by(TicketDAO.id).first()

    if not next_ticket:
        raise HTTPException(status_code=404, detail="No customers waiting")

    next_ticket.status = "served"
    db.commit()
    db.refresh(next_ticket)

    service_dto = ServiceDTO(
        service_id=next_ticket.service.id,
        service_name=next_ticket.service.name,
        description=next_ticket.service.description
    )

    return NextCustomerResponseDTO(
        counter_id=request.counter_id,
        customer_id=next_ticket.id,
        service=service_dto
    )
