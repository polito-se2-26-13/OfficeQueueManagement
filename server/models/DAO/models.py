from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# maps to the 'services' table
class ServiceDAO(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    prefix = Column(String, default="S")  # used for ticket codes e.g. S001

    tickets = relationship("TicketDAO", back_populates="service")


# maps to the 'tickets' table
class TicketDAO(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    status = Column(String, default="waiting")  # waiting or served
    service_id = Column(Integer, ForeignKey('services.id'))

    service = relationship("ServiceDAO", back_populates="tickets")
