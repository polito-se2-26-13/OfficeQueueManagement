from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship
from server.database import Base

class CounterDAO(Base):
    __tablename__="counter"

    counter_id=Column(Integer,primary_key=True, autoincrement=True)
    position=Column(Integer, nullable=False)

#relationship(nameDAO,attr. of relation in other dao)
    counter_services=relationship("CouterServiceDAO",back_populates="counter")