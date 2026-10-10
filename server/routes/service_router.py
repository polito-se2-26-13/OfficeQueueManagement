from typing import List

from fastapi import APIRouter, status

from server.models.DTO.service_dto import ServiceDTO
from server.controllers.service_controller import ServiceController
from server.config.config import ROUTES

router = APIRouter(prefix=ROUTES["SERVICE"], tags=["Service"])
controller = ServiceController()


@router.get(
    "/",
    response_model=List[ServiceDTO],
    status_code=status.HTTP_200_OK,
)
def get_services():
    """GET /api/services — Return the list of all available services."""
    return controller.get_service_list()
