"""Integration tests of the Next customer story: POST /api/counters/{id}/next-customer."""
import pytest

from server.models.DAO.counter_dao import CounterDAO
from server.models.DAO.counter_service_dao import CouterServiceDAO
from server.models.DAO.service_dao import ServiceDAO


def add_service(db, name):
    service = ServiceDAO(name=name, description=f"{name} desk")
    db.add(service)
    db.commit()
    return service.service_id


def add_counter(db, position, service_ids):
    counter = CounterDAO(position=position)
    db.add(counter)
    db.flush()
    for service_id in service_ids:
        db.add(CouterServiceDAO(counter_id=counter.counter_id, service_id=service_id))
    db.commit()
    return counter.counter_id


@pytest.fixture
def office(db):
    """Customer Support and Payments, both served by counter 1."""
    support = add_service(db, "Customer Support")
    payments = add_service(db, "Payments")
    counter = add_counter(db, 1, [support, payments])
    return {"support": support, "payments": payments, "counter": counter}


def take_ticket(client, service_id):
    return client.post("/api/tickets", json={"service_id": service_id}).json()


def call_next(client, counter_id):
    return client.post(f"/api/counters/{counter_id}/next-customer")


def test_unknown_counter_returns_404(client):
    response = call_next(client, 99)

    assert response.status_code == 404
    assert response.json() == {"detail": "Counter with id 99 not found"}


def test_empty_queues_return_204(client, office):
    response = call_next(client, office["counter"])

    assert response.status_code == 204


def test_calls_a_ticket_of_a_service_the_counter_serves(client, office):
    ticket = take_ticket(client, office["support"])

    response = call_next(client, office["counter"])

    assert response.status_code == 200
    assert response.json() == {
        "ticket_id": ticket["ticket_id"],
        "ticket_cod": ticket["ticket_cod"],
        "service": {
            "service_id": office["support"],
            "service_name": "Customer Support",
            "description": "Customer Support desk",
        },
        "counter": {"counter_id": office["counter"], "position": 1},
    }


def test_counter_ignores_services_it_does_not_serve(client, db, office):
    payments_only = add_counter(db, 2, [office["payments"]])
    take_ticket(client, office["support"])

    response = call_next(client, payments_only)

    assert response.status_code == 204


def test_counter_without_services_returns_204(client, db, office):
    idle = add_counter(db, 2, [])
    take_ticket(client, office["support"])

    response = call_next(client, idle)

    assert response.status_code == 204


def test_longest_queue_goes_first(client, office):
    take_ticket(client, office["support"])
    first_payment = take_ticket(client, office["payments"])
    take_ticket(client, office["payments"])
    take_ticket(client, office["payments"])

    response = call_next(client, office["counter"])

    assert response.json()["ticket_cod"] == first_payment["ticket_cod"]


def test_tie_goes_to_the_queue_waiting_longest(client, office):
    # temporary rule: the requirements break ties with the lowest service time, which services do not have yet
    first_payment = take_ticket(client, office["payments"])
    take_ticket(client, office["support"])
    take_ticket(client, office["support"])
    take_ticket(client, office["payments"])

    response = call_next(client, office["counter"])

    assert response.json()["ticket_cod"] == first_payment["ticket_cod"]


def test_called_ticket_leaves_the_queue(client, office):
    take_ticket(client, office["support"])

    first_call = call_next(client, office["counter"])
    second_call = call_next(client, office["counter"])

    assert first_call.status_code == 200
    assert second_call.status_code == 204