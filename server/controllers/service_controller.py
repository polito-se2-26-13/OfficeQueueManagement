from server.repositories.service_repository import ServiceRepository
from server.service.mapper_service import serviceDAO_to_responseDTO


class ServiceController:
    def __init__(self):
        self.repo = ServiceRepository()

    def get_service_list(self):
        daos = self.repo.get_service_list()
        return [serviceDAO_to_responseDTO(dao) for dao in daos]
