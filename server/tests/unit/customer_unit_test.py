import pytest
from unittest.mock import MagicMock, patch

from server.controllers.counter_controller import CounterController
from server.repositories.counter_reposotory import CounterRepository
from server.service.mapper_service import next_customerDAO_to_ResponseDTO
from server.models.DAO.ticket_dao import TicketDAO
from server.models.DAO.service_dao import ServiceDAO
from server.models.DAO.counter_dao import CounterDAO
from server.models.DAO.counter_service_dao import CouterServiceDAO


# ============================================================
# 1. MAPPER TESTS
# ============================================================

class TestCounterMapperService:
    """Test the next customer DAO -> DTO mapping."""

    def test_next_customer_dao_to_dto_maps_all_fields(self):
        """Test that ticket, service and counter are correctly
        mapped to NextCustomerDTO.
        """

        # Arrange
        fake_ticket = MagicMock()
        fake_ticket.ticket_id =12
        fake_ticket.ticket_cod = "S012"

        fake_service = MagicMock()
        fake_service.service_id = 10
        fake_service.name = "Saving"
        fake_service.description = "Saving description"

        fake_counter = MagicMock()
        fake_counter.counter_id = 2
        fake_counter.position = 5

        # Act
        result = next_customerDAO_to_ResponseDTO(
            fake_ticket,
            fake_service,
            fake_counter
        )

        # Assert
        assert result.ticket_id == 12
        assert result.ticket_cod == "S012"

        assert result.service.service_id == 10
        assert result.service.service_name == "Saving"
        assert result.service.description == "Saving description"

        assert result.counter.counter_id == 2
        assert result.counter.position == 5


# ============================================================
# 2. CONTROLLER TESTS
# ============================================================

class TestCounterController:
    """Test CounterController.get_next_customer()."""

    @patch(
        "server.controllers.counter_controller.next_customerDAO_to_ResponseDTO"
    )
    @patch(
        "server.controllers.counter_controller.CounterRepository"
    )
    def test_get_next_customer_success(
        self,
        mock_repo_cls,
        mock_mapper
    ):
        """Test successfully returning the next customer."""

        # Arrange
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo

        fake_ticket = MagicMock()
        fake_service = MagicMock()
        fake_counter = MagicMock()

        mock_repo.get_next_customer.return_value = (
            fake_ticket,
            fake_service,
            fake_counter
        )

        expected_response = MagicMock()
        mock_mapper.return_value = expected_response

        # Act
        controller = CounterController()
        result = controller.get_next_customer(id_counter=1)

        # Assert
        assert result == expected_response

        mock_repo.get_next_customer.assert_called_once_with(1)

        mock_mapper.assert_called_once_with(
            fake_ticket,
            fake_service,
            fake_counter
        )

    @patch(
        "server.controllers.counter_controller.CounterRepository"
    )
    def test_get_next_customer_no_customer(
        self,
        mock_repo_cls
    ):
        """Test that None is returned when no customer is waiting."""

        # Arrange
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo

        mock_repo.get_next_customer.return_value = None

        # Act
        controller = CounterController()
        result = controller.get_next_customer(id_counter=1)

        # Assert
        assert result is None

        mock_repo.get_next_customer.assert_called_once_with(1)
# ============================================================
# 3. REPOSITORY TESTS
# ============================================================

class TestCounterRepository:
    """Test CounterRepository.get_next_customer()."""

    def test_get_next_customer_success(self):
        """Test returning a waiting ticket for a counter."""

        # Arrange
        mock_session = MagicMock()

        fake_ticket = MagicMock()
        fake_ticket.ticket_id = 1
        fake_ticket.ticket_cod = "S001"

        fake_service = MagicMock()
        fake_service.service_id = 10
        fake_service.name = "Saving"
        fake_service.description = "Saving description"

        fake_counter = MagicMock()
        fake_counter.counter_id = 1

        fake_row = (
            fake_ticket,
            fake_service,
            fake_counter
        )

        mock_session.execute.return_value.first.return_value = fake_row

        repo = CounterRepository(session=mock_session)

        # Act
        result = repo.get_next_customer(id_counter=1)

        # Assert
        assert result is not None

        ticket, service, counter = result

        assert ticket == fake_ticket
        assert service == fake_service
        assert counter == fake_counter

        mock_session.execute.assert_called_once()

        mock_session.expunge.assert_any_call(fake_ticket)
        mock_session.expunge.assert_any_call(fake_service)
        mock_session.expunge.assert_any_call(fake_counter)

    def test_get_next_customer_no_waiting_customer(self):
        """Test returning None when there is no waiting customer."""

        # Arrange
        mock_session = MagicMock()

        mock_session.execute.return_value.first.return_value = None

        repo = CounterRepository(session=mock_session)

        # Act
        result = repo.get_next_customer(id_counter=1)

        # Assert
        assert result is None
        mock_session.execute.assert_called_once()
        mock_session.expunge.assert_not_called()

