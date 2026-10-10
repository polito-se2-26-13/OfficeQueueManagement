from server.repositories.ticket_repository import TicketRepository
from server.service.mapper_service import ticketDAO_to_responseDTO


class TicketController:
    def __init__(self):
        self.repo = TicketRepository()

    def create_ticket(self, service_id: int):
        """
        Returns a TicketResponseDTO on success, or None if the service doesn't exist.
        """
        result = self.repo.create_ticket(service_id)
        if result is None:
            return None
        ticket, service = result
        return ticketDAO_to_responseDTO(ticket, service)
