from typing import Optional
from server.const import WAITING
from sqlalchemy import select
from sqlalchemy.orm import Session
from server.models.DAO.counter_dao import CounterDAO
from server.models.DAO.service_dao import ServiceDAO
from server.models.DAO.ticket_dao import TicketDAO
from server.models.DAO.counter_service_dao import CouterServiceDAO
from server.database import SessionLocal


class CounterRepository:
    def __init__(self, session: Optional[Session] = None):
        self.session = session

    def _get_session(self) -> Session:
        return self.session or SessionLocal()

    def get_counter_list(self) -> list[CounterDAO]:
        """Get all counters."""
        session = self._get_session()
        try:
            result = session.scalars(select(CounterDAO))
            items = result.all()
            for item in items:
                session.expunge(item)
            return items
        finally:
            if self.session is None:
                session.close()

    def get_next_customer(self, id_counter: int) -> tuple[TicketDAO, ServiceDAO, CounterDAO] | None:
        """Return the oldest waiting ticket for the given counter, or None."""
        session = self._get_session()
        try:
            row = session.execute(
                select(TicketDAO, ServiceDAO, CounterDAO)
                .join(ServiceDAO, TicketDAO.service_id == ServiceDAO.service_id)
                .join(CouterServiceDAO, ServiceDAO.service_id == CouterServiceDAO.service_id)
                .join(CounterDAO, CounterDAO.counter_id == CouterServiceDAO.counter_id)
                .where(
                    CouterServiceDAO.counter_id == id_counter,
                    TicketDAO.status == WAITING,
                )
                .order_by(TicketDAO.created_time.asc(), TicketDAO.ticket_cod.asc())
            ).first()

            if row is None:
                return None

            ticket, service, counter = row
            session.expunge(ticket)
            session.expunge(service)
            session.expunge(counter)
            return ticket, service, counter
        finally:
            if self.session is None:
                session.close()