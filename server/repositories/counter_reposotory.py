from typing import Optional
from server.const import WAITING
from sqlalchemy import select, func
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

    def counter_exists(self, id_counter: int) -> bool:
        """True if a counter with the given id exists."""
        session = self._get_session()
        try:
            return session.get(CounterDAO, id_counter) is not None
        finally:
            if self.session is None:
                session.close()

    def get_next_customer(self, id_counter: int) -> tuple[TicketDAO, ServiceDAO, CounterDAO] | None:
        """Return the first ticket of the longest queue the counter serves, or None. Ties go to the queue whose first ticket arrived earlier, until services have a service time."""
        session = self._get_session()
        try:
            longest_queue = session.scalar(
                select(TicketDAO.service_id)
                .join(CouterServiceDAO, TicketDAO.service_id == CouterServiceDAO.service_id)
                .where(
                    CouterServiceDAO.counter_id == id_counter,
                    TicketDAO.status == WAITING,
                )
                .group_by(TicketDAO.service_id)
                .order_by(func.count().desc(), func.min(TicketDAO.created_time).asc())
                .limit(1)
            )
            if longest_queue is None:
                return None

            row = session.execute(
                select(TicketDAO, ServiceDAO, CounterDAO)
                .join(ServiceDAO, TicketDAO.service_id == ServiceDAO.service_id)
                .join(CouterServiceDAO, ServiceDAO.service_id == CouterServiceDAO.service_id)
                .join(CounterDAO, CounterDAO.counter_id == CouterServiceDAO.counter_id)
                .where(
                    CouterServiceDAO.counter_id == id_counter,
                    TicketDAO.status == WAITING,
                    TicketDAO.service_id == longest_queue,
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