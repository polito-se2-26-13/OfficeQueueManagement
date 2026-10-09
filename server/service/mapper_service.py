from server.models.DAO.counter_dao import CounterDAO
from server.models.DAO.service_dao import ServiceDAO
from server.models.DAO.ticket_dao import TicketDAO

from server.models.DTO.couter_dto import GetCounterDTO, CounterDTO, NextCustomerDTO
from server.models.DTO.service_dto import ServiceDTO
from server.models.DTO.ticket_dto import TicketResponseDTO


def counterDAO_to_responseDTO(counter_dao: CounterDAO) -> GetCounterDTO:
    return GetCounterDTO(counter_id=counter_dao.counter_id)


# keep old name as alias so existing code still works
counterDao_to_responseDTO = counterDAO_to_responseDTO


def serviceDAO_to_responseDTO(service_dao: ServiceDAO) -> ServiceDTO:
    return ServiceDTO(
        service_id=service_dao.service_id,
        service_name=service_dao.name,
        description=service_dao.description,
    )


def ticketDAO_to_responseDTO(ticket_dao: TicketDAO, service_dao: ServiceDAO) -> TicketResponseDTO:
    return TicketResponseDTO(
        ticket_id=ticket_dao.ticket_id,
        ticket_cod=ticket_dao.ticket_cod,
        service_name=service_dao.name,
        timeStamp=str(ticket_dao.created_time),
    )


def next_customerDAO_to_ResponseDTO(
    ticket_dao: TicketDAO,
    service_dao: ServiceDAO,
    counter_dao: CounterDAO,
) -> NextCustomerDTO:
    return NextCustomerDTO(
        ticket_id=ticket_dao.ticket_id,
        ticket_cod=ticket_dao.ticket_cod,
        service=ServiceDTO(
            service_id=service_dao.service_id,
            service_name=service_dao.name,
            description=service_dao.description,
        ),
        counter=CounterDTO(
            counter_id=counter_dao.counter_id,
            position=counter_dao.position,
        ),
    )