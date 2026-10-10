from pydantic import BaseModel


class TicketRequestDTO(BaseModel):
    """Body for POST /api/tickets"""
    service_id: int


class TicketResponseDTO(BaseModel):
    """201 response for POST /api/tickets"""
    ticket_id: int
    ticket_cod: str       # e.g. C001, P002
    service_name: str
    timeStamp: str        # HH:MM:SS as string
