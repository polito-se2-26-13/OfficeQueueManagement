from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship
from server.database import Base

class TicketDAO(Base):
    __tablename__="tickets"
    
    ticket_id=Column(Integer,primary_key=True,autoincrement=True)
    ticket_cod=Column(String,nullable=False)
    service_id=Column(Integer,  ForeignKey("services.service_id"),nullable=False)
    status = Column(String, nullable=False)
    created_time = Column(Time, nullable=False)

    #relationship(nameDAO,attr. of relation in other dao)
    service=relationship("ServiceDAO",back_populates="tickets")
