from pytest import fixture
from unittest.mock import MagicMock
from users_service.service import UsersService
from database_service.__test__.mocks.mock_service import mock_database_service
from database_service.unique_id_generator_service.__test__.mocks.mock_service import mock_id_generator_service


@fixture()
def mock_users_service():
    users_service = UsersService(mock_database_service(), mock_id_generator_service())
    users_service.create_one = MagicMock(return_value = {})
    users_service.update_one = MagicMock(return_value = {})
    users_service.get_one = MagicMock(return_value = {})
    users_service.get_all = MagicMock(return_value = [])
    return users_service
