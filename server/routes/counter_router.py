from typing import List
from fastapi import APIRouter, Response, status, HTTPException
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
    status_code=status.HTTP_200_OK,
    responses={
        204: {"description": "No customer waiting"},
        404: {"description": "Counter not found"}
    },
)
def post_next_customer(id_counter:int):
    """search next customer"""
    if not controller.counter_exists(id_counter):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Counter with id {id_counter} not found",
        )
    DTO=controller.get_next_customer(id_counter)
    if DTO is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return DTO