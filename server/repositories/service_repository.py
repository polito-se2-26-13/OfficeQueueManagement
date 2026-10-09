from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from server.models.DAO.service_dao import ServiceDAO
from server.database import SessionLocal


class ServiceRepository:
    def __init__(self, session: Optional[Session] = None):
        self.session = session

    def _get_session(self) -> Session:
        return self.session or SessionLocal()

    def get_service_list(self) -> list[ServiceDAO]:
        """Return all services."""
        session = self._get_session()
        try:
            items = session.scalars(select(ServiceDAO)).all()
            for item in items:
                session.expunge(item)
            return items
        finally:
            if self.session is None:
                session.close()

    def get_service_by_id(self, service_id: int) -> Optional[ServiceDAO]:
        """Return a single service or None."""
        session = self._get_session()
        try:
            obj = session.get(ServiceDAO, service_id)
            if obj is not None:
                session.expunge(obj)
            return obj
        finally:
            if self.session is None:
                session.close()
