from unittest.mock import AsyncMock, MagicMock, patch

@patch('database_service.service.DatabaseService')
@patch('database_service.service.unique_id_generator_service')
async def test_create_one(mock_database_service, mock_id_generator_service):
    pass

async def test_get_one():
    pass

async def test_get_all():
    pass

async def test_update_one():
    pass

async def test_delete_one():
    pass
