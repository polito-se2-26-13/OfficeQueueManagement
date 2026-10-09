from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship
from server.database import Base

class CouterServiceDAO(Base):
    __tablename__="counter_services"

    counter_id=Column(Integer,ForeignKey("counter.counter_id"),primary_key=True,nullable=False)
    service_id=Column(Integer,ForeignKey("services.service_id"),primary_key=True,nullable=False)

#relationship(nameDAO,attr. of relation in other dao)
    service=relationship("ServiceDAO",back_populates="counter_services")
    counter=relationship("CounterDAO",back_populates="counter_services")