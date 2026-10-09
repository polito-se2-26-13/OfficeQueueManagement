from datetime import datetime
from typing import Optional
from sqlalchemy import select, func
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
        ticket_cod = first letter of service name + 3-digit sequence (e.g. C001).
        Returns (new TicketDAO, ServiceDAO) or None if the service doesn't exist.
        """
        session = self._get_session()
        try:
            service = session.get(ServiceDAO, service_id)
            if service is None:
                return None

            # count existing tickets for this service to form the next code
            count = session.scalar(
                select(func.count()).where(TicketDAO.service_id == service_id)
            ) or 0
            prefix = service.name[0].upper()
            ticket_cod = f"{prefix}{count + 1:03d}"

            now = datetime.now().time()
            new_ticket = TicketDAO(
                ticket_cod=ticket_cod,
                service_id=service_id,
                status=WAITING,
                created_time=now,
            )
            session.add(new_ticket)
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
