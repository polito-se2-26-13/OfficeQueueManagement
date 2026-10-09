from server.repositories.counter_reposotory import CounterRepository
from server.service.mapper_service import counterDao_to_responseDTO,next_customerDAO_to_ResponseDTO

class CounterController():
    def __init__(self):
        self.repo=CounterRepository()

    def get_counter_list(self):
        daos= self.repo.get_counter_list();
        return  [counterDao_to_responseDTO(dao) for dao in daos]

    def get_next_customer(self,id_counter:int):
        dao=self.repo.get_next_customer(id_counter)
        if dao is None:
            return None
        else:
            ticket,service,counter=dao
            return next_customerDAO_to_ResponseDTO(ticket,service,counter)