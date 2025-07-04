from unittest.mock import AsyncMock, MagicMock, patch
from pytest import fixture
from database_service.service import DatabaseService

@fixture()
def mock_database_service():
    database_service = DatabaseService(None)
    database_service.get_one = AsyncMock(return_value={})
    database_service.get_all = AsyncMock(return_value=[])
    database_service.create_one = AsyncMock(return_value={})
    database_service.update_one = AsyncMock(return_value={})
    database_service.delete_one = AsyncMock(return_value=None)
    return database_service