from typing import  Optional
from server.const import WAITING
from sqlalchemy import select
from sqlalchemy.orm import Session
from server.models.DAO.counter_dao import CounterDAO
from server.models.DAO.service_dao import ServiceDAO 
from server.models.DAO.ticket_dao import TicketDAO 
from server.models.DAO.counter_service_dao import CouterServiceDAO
from server.database import SessionLocal

class CounterRepository:
    def __init__(self, session:Optional[Session]=None):
        self.session=session

    def  _get_session(self):
        return self.session or SessionLocal()

    def get_counter_list(self)->list[CounterDAO]:
        """Get all counter"""
        with self._get_session() as session:
            result=session.scalars(select(CounterDAO)) 
            return result.all()

    def get_next_customer(self,id_counter:int)->tuple[TicketDAO, ServiceDAO, CounterDAO]|None:
        with self._get_session() as session:
            result=session.execute(select(TicketDAO,ServiceDAO,CounterDAO)
                .join(ServiceDAO, TicketDAO.service_id== ServiceDAO.service_id)
                .join(CouterServiceDAO, ServiceDAO.service_id==CouterServiceDAO.service_id)
                .join(CounterDAO,CounterDAO.counter_id==CouterServiceDAO.counter_id)
                .where(id_counter==CouterServiceDAO.counter_id, TicketDAO.status==WAITING)
                .order_by(TicketDAO.created_time.asc(),TicketDAO.ticket_cod.asc())                      
            ).first()

            return result