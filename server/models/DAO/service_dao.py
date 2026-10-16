from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship
from server.database import Base

class ServiceDAO(Base):
    __tablename__="services"

    service_id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String, nullable=False)
    description=Column(String,nullable=False)

#relationship(nameDAO,attr. of relation in other dao)
    tickets = relationship("TicketDAO", back_populates="service")
    counter_services=relationship("CouterServiceDAO",back_populates="service")
