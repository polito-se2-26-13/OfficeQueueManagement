from typing import List
from fastapi import APIRouter, Response, status
from server.models.DTO.couter_dto import GetCounterDTO,NextCustomerDTO
from server.controllers.counter_controller import CounterController
from server.config.config import ROUTES

router = APIRouter(prefix=ROUTES["COUNTER"], tags=["Counter"])
controller=CounterController()

@router.get(
    "/",
    response_model=List[GetCounterDTO],
    status_code=status.HTTP_200_OK
)
def get_customer():
    """Return a list of couter"""
    return controller.get_counter_list()

@router.post(
    "/{id_counter}/next-customer",
    response_model=NextCustomerDTO,
    status_code=status.HTTP_200_OK
)
def post_next_customer(id_counter:int):
    """search next customer"""
    DTO=controller.get_next_customer(id_counter)
    if DTO is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return DTO