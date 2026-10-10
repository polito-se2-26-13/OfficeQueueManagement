from fastapi import APIRouter, HTTPException, status

from server.models.DTO.ticket_dto import TicketRequestDTO, TicketResponseDTO
from server.controllers.ticket_controller import TicketController
from server.config.config import ROUTES

router = APIRouter(prefix=ROUTES["TICKET"], tags=["Ticket"])
controller = TicketController()


@router.post(
    "/",
    response_model=TicketResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(body: TicketRequestDTO):
    """POST /api/tickets — Issue a new ticket for the given service."""
    dto = controller.create_ticket(body.service_id)
    if dto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service with id {body.service_id} not found",
        )
    return dto
