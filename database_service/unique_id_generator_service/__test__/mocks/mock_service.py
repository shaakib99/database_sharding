from unittest.mock import AsyncMock, MagicMock, patch
from pytest import fixture
from database_service.unique_id_generator_service.service import IDGeneratorService

@fixture()
def mock_id_generator_service():
    id_generator_service = IDGeneratorService()
    id_generator_service.generate = AsyncMock(return_value={})
    id_generator_service._get_epoch_ms = AsyncMock(return_value={})
    id_generator_service._hash = AsyncMock(return_value={})
    id_generator_service._prefix_to_int = AsyncMock(return_value=[])
    return id_generator_service