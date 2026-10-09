from pydantic import BaseModel
from typing import List


class ServiceDTO(BaseModel):
    service_id: int
    service_name: str
    description: str

    class Config:
        from_attributes = True  # lets us build this from a SQLAlchemy object


class ServicesResponseDTO(BaseModel):
    services: List[ServiceDTO]


class TicketRequestDTO(BaseModel):
    service_id: int  # which service the customer needs


class TicketResponseDTO(BaseModel):
    ticket_id: int
    ticket_code: str  # e.g. S001, A003

    class Config:
        from_attributes = True


class NextCustomerRequestDTO(BaseModel):
    counter_id: int  # which counter is calling the next customer


class NextCustomerResponseDTO(BaseModel):
    counter_id: int
    customer_id: int
    service: ServiceDTO
