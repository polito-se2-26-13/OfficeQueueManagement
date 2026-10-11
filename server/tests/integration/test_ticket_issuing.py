"""Integration tests of the Get ticket story (OQM-2): GET /api/services and POST /api/tickets."""

from server.models.DAO.service_dao import ServiceDAO
from server.models.DAO.ticket_dao import TicketDAO


def add_service(db, name):
    service = ServiceDAO(name=name, description=f"{name} desk")
    db.add(service)
    db.commit()
    return service.service_id


def test_services_empty(client):
    response = client.get("/api/services")

    assert response.status_code == 200
    assert response.json() == []


def test_services_come_from_the_database(client, db):
    shipping = add_service(db, "Shipping")
    payments = add_service(db, "Payments")

    response = client.get("/api/services")

    assert response.status_code == 200
    assert response.json() == [
        {"service_id": shipping, "service_name": "Shipping", "description": "Shipping desk"},
        {"service_id": payments, "service_name": "Payments", "description": "Payments desk"},
    ]


def test_new_ticket_is_saved_as_waiting(client, db):
    shipping = add_service(db, "Shipping")

    response = client.post("/api/tickets", json={"service_id": shipping})

    assert response.status_code == 201
    ticket = response.json()
    assert ticket["ticket_cod"] == "S001"
    assert ticket["service_name"] == "Shipping"
    saved = db.get(TicketDAO, ticket["ticket_id"])
    assert saved.service_id == shipping
    assert saved.status == "WAITING"


def test_each_ticket_gets_a_new_code(client, db):
    shipping = add_service(db, "Shipping")
    payments = add_service(db, "Payments")

    first = client.post("/api/tickets", json={"service_id": shipping}).json()
    second = client.post("/api/tickets", json={"service_id": shipping}).json()
    other = client.post("/api/tickets", json={"service_id": payments}).json()

    assert first["ticket_cod"].startswith("S")
    assert second["ticket_cod"].startswith("S")
    assert other["ticket_cod"].startswith("P")
    assert first["ticket_cod"] != second["ticket_cod"]


def test_ticket_for_unknown_service(client):
    response = client.post("/api/tickets", json={"service_id": 99})

    assert response.status_code == 404
    assert "detail" in response.json()


def test_ticket_without_service_id(client):
    response = client.post("/api/tickets", json={})

    assert response.status_code == 422


def test_codes_are_unique_with_the_same_initial(client, db):
    shipping = add_service(db, "Shipping")
    savings = add_service(db, "Savings")

    first = client.post("/api/tickets", json={"service_id": shipping}).json()
    second = client.post("/api/tickets", json={"service_id": savings}).json()

    assert first["ticket_cod"] != second["ticket_cod"]
