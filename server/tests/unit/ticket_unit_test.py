import pytest
from unittest.mock import MagicMock, patch

from server.controllers.ticket_controller import TicketController
from server.service.mapper_service import ticketDAO_to_responseDTO
from server.repositories.ticket_repository import TicketRepository
from server.models.DAO.service_dao import ServiceDAO
from server.models.DAO.counter_service_dao import CouterServiceDAO
from datetime import time


# ============================================================
# 1. MAPPER TESTS
# ============================================================

class TestTicketMapperService:
    """Test the ticketDAO_to_responseDTO mapper function."""

    def test_ticket_dao_to_dto_maps_all_fields(self):
        """Test that ticket DAO and service DAO are correctly mapped
        to TicketResponseDTO.
        """
        # Arrange
        fake_ticket = MagicMock()
        fake_ticket.ticket_id = 1
        fake_ticket.ticket_cod = "C001"
        fake_ticket.created_time = time(10, 30, 0)

        fake_service = MagicMock()
        fake_service.name = "Consulting"

        # Act
        result = ticketDAO_to_responseDTO(
            fake_ticket,
            fake_service
        )

        # Assert
        assert result.ticket_id == 1
        assert result.ticket_cod == "C001"
        assert result.service_name == "Consulting"
        assert result.timeStamp == "10:30:00"


# ============================================================
# 2. CONTROLLER TESTS
# ============================================================

class TestTicketController:
    """Test the TicketController.create_ticket method."""

    @patch("server.controllers.ticket_controller.ticketDAO_to_responseDTO")
    @patch("server.controllers.ticket_controller.TicketRepository")
    def test_create_ticket_success(
        self,
        mock_repo_cls,
        mock_mapper
    ):
        """Test successfully creating a ticket."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo

        fake_ticket = MagicMock()
        fake_service = MagicMock()

        mock_repo.create_ticket.return_value = (
            fake_ticket,
            fake_service
        )

        expected_response = MagicMock()
        mock_mapper.return_value = expected_response

        # Act
        controller = TicketController()
        result = controller.create_ticket(service_id=1)

        # Assert
        assert result == expected_response

        mock_repo.create_ticket.assert_called_once_with(1)

        mock_mapper.assert_called_once_with(
            fake_ticket,
            fake_service
        )

    @patch("server.controllers.ticket_controller.TicketRepository")
    def test_create_ticket_service_not_found(
        self,
        mock_repo_cls
    ):
        """Test that None is returned when the service does not exist."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo

        mock_repo.create_ticket.return_value = None

        # Act
        controller = TicketController()
        result = controller.create_ticket(service_id=999)

        # Assert
        assert result is None

        mock_repo.create_ticket.assert_called_once_with(999)

    @patch("server.controllers.ticket_controller.TicketRepository")
    def test_create_ticket_repository_exception(
        self,
        mock_repo_cls
    ):
        """Test that a repository exception is propagated."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo

        mock_repo.create_ticket.side_effect = RuntimeError(
            "Database error"
        )

        # Act + Assert
        controller = TicketController()

        with pytest.raises(RuntimeError):
            controller.create_ticket(service_id=1)

# ==========================================
# 3. TicketRepository 
# ==========================================

class TestTicketRepository:
    def test_create_ticket_service_not_found(self):
        """Test returning None when the service does not exist."""
        mock_session = MagicMock()
        mock_session.get.return_value = None  

        repo = TicketRepository(session=mock_session)
        result = repo.create_ticket(service_id=999)

        assert result is None
        mock_session.get.assert_called_once_with(ServiceDAO, 999)

    def test_create_first_ticket(self):
        """Test creating the first ticket for a service."""
        mock_session = MagicMock()

        fake_service = MagicMock()
        fake_service.service_id = 1
        fake_service.name = "Consulting"
        fake_service.description = "Consulting description"

        mock_session.get.return_value = fake_service

    # Simulate the database assigning ticket_id = 1
        def assign_ticket_id(ticket):
          ticket.ticket_id = 1

        mock_session.flush.side_effect = assign_ticket_id

        repo = TicketRepository(session=mock_session)
        ticket, returned_service = repo.create_ticket(service_id=1)

        assert ticket.ticket_cod == "C001"
        assert ticket.service_id == 1
        assert ticket.status == "WAITING"


    def test_create_ticket_success_formatting(self):
        """Test creating a ticket successfully with the correct format (uppercase first letter + 3-digit serial number)."""
        mock_session = MagicMock()
        
        # Mock service data using MagicMock instead of instantiating an actual SQLAlchemy model
        fake_service = MagicMock()
        fake_service.service_id = 1
        fake_service.name = "Consulting"
        fake_service.description = "Consulting description"
        mock_session.get.return_value = fake_service
        
        # Simulate the database assigning ticket_id = 3
        def assign_ticket_id(ticket):
          ticket.ticket_id = 3
        mock_session.flush.side_effect = assign_ticket_id
        repo = TicketRepository(session=mock_session)
        ticket, returned_service = repo.create_ticket(service_id=1)

        assert returned_service.service_id == 1
        assert ticket.ticket_cod == "C003"
        assert ticket.service_id == 1
        assert ticket.status == "WAITING"
        
        # Verify that database transaction operations are called
        mock_session.add.assert_called_once()
        mock_session.flush.assert_called_once()
        mock_session.commit.assert_called_once()
       