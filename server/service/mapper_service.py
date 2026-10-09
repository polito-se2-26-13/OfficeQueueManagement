from server.models.DAO.counter_dao import CounterDAO
from server.models.DTO.couter_dto import GetCounterDTO, CounterDTO, NextCustomerDTO
from server.models.DAO.service_dao import ServiceDAO
from server.models.DTO.service_dto import ServiceDTO
from server.models.DAO.ticket_dao import TicketDAO 
from server.models.DAO.counter_service_dao import CouterServiceDAO


def counterDao_to_responseDTO(counter_dao:CounterDAO)->GetCounterDTO:
    return GetCounterDTO(
        counter_id=counter_dao.counter_id
    )
def next_customerDAO_to_ResponseDTO(ticket_dao:TicketDAO,service_dao:ServiceDAO,counter_dao:CounterDAO)->NextCustomerDTO:
    return NextCustomerDTO(
        ticket_id=ticket_dao.ticket_id,
        ticket_cod=ticket_dao.ticket_cod,
        service=ServiceDTO(
            service_id=service_dao.service_id,
            service_name=service_dao.name,
            description=service_dao.description
        ),
        counter=CounterDTO(
            counter_id=counter_dao.counter_id,
            position= counter_dao.position
        )
    )