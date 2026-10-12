from pydantic import BaseModel
from server.models.DTO.service_dto import ServiceDTO
class GetCounterDTO(BaseModel):
    counter_id: int

class CounterDTO(BaseModel):
    counter_id: int
    position: int

class NextCustomerDTO(BaseModel):
    ticket_id: int
    ticket_cod: str
    service: ServiceDTO
    counter: CounterDTO