from server.repositories.counter_reposotory import CounterRepository
from server.service.mapper_service import counterDao_to_responseDTO,next_customerDAO_to_ResponseDTO
from server.const import StatusTicket

class CounterController():
    def __init__(self):
        self.repo=CounterRepository()

    def get_counter_list(self):
        daos= self.repo.get_counter_list();
        return  [counterDao_to_responseDTO(dao) for dao in daos]

    def counter_exists(self,id_counter:int) -> bool:
        return self.repo.counter_exists(id_counter)

    def get_next_customer(self,id_counter:int):
        daos=self.repo.get_next_customer(id_counter)
        if daos is None:
            return None
        else:
            ticket,service,counter=daos
            self.repo.update_ticket_status(ticket.ticket_id,StatusTicket.INPROGRESS)
            return next_customerDAO_to_ResponseDTO(ticket,service,counter)
