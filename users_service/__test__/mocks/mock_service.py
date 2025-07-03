from pytest import fixture
from unittest.mock import MagicMock
from users_service.service import UsersService


@fixture()
def mock_users_service():
    users_service = UsersService()
    users_service.create_one = MagicMock(return_value = {})
    users_service.update_one = MagicMock(return_value = {})
    users_service.get_one = MagicMock(return_value = {})
    users_service.get_all = MagicMock(return_value = {})
    return users_service
