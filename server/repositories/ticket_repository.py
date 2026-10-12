from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from server.models.DAO.ticket_dao import TicketDAO
from server.models.DAO.service_dao import ServiceDAO
from server.database import SessionLocal
from server.const import WAITING


class TicketRepository:
    def __init__(self, session: Optional[Session] = None):
        self.session = session

    def _get_session(self) -> Session:
        return self.session or SessionLocal()

    def create_ticket(self, service_id: int) -> Optional[tuple[TicketDAO, ServiceDAO]]:
        """
        Generate a new ticket for the given service.
        ticket_cod = first letter of service name + ticket_id with 3 digits (e.g. C001).
        Returns (new TicketDAO, ServiceDAO) or None if the service doesn't exist.
        """
        session = self._get_session()
        try:
            service = session.get(ServiceDAO, service_id)
            if service is None:
                return None

            now = datetime.now().time()
            new_ticket = TicketDAO(
                ticket_cod="", # to be generated
                service_id=service_id,
                status=WAITING,
                created_time=now,
            )
            session.add(new_ticket)
            # flush sends the INSERT without committing, so the database assigns ticket_id now
            session.flush()
            # ticket_id is unique in the whole table, so the code is unique for the whole office

            prefix = service.name[0].upper()
            new_ticket.ticket_cod = f"{prefix}{new_ticket.ticket_id:03d}"
            session.commit()

            session.refresh(new_ticket)
            session.refresh(service)

            # detach before returning so they survive session close
            session.expunge(new_ticket)
            session.expunge(service)
            return new_ticket, service
        finally:
            if self.session is None:
                session.close()
