from database_service.__test__.mocks.mock_service import mock_database_service
from database_service.unique_id_generator_service.__test__.mocks.mock_service import mock_id_generator_service
from users_service.service import UsersService
from users_service.models import CreateUserModel, UpdateUserModel
from database_service.models import QueryModel


async def test_create_one():
    users_service = UsersService(mock_database_service(), mock_id_generator_service())
    create_user_model = CreateUserModel(
        username="test_user",
        email="test@email.com",
        password="securepassword",
    )
    result = await users_service.create_one(create_user_model)
    assert result.id is not None, "User ID should not be None"
    assert result.username == create_user_model.username, "Username should match the input"
    assert result.email == create_user_model.email, "Email should match the input"

async def test_get_one():
    users_service = UsersService(mock_database_service(), mock_id_generator_service())
    user_id = "test_user_id"
    result = await users_service.get_one(user_id)
    assert result is not None, "User should not be None"
    assert result.id == user_id, "User ID should match the input ID"


async def test_get_all():
    users_service = UsersService(mock_database_service(), mock_id_generator_service())
    result = await users_service.get_all(QueryModel())
    assert isinstance(result, list), "Result should be a list"
    assert all(hasattr(user, 'id') for user in result), "All users should have an ID attribute"

async def test_update_one():
    users_service = UsersService(mock_database_service(), mock_id_generator_service())
    user_id = "test_user_id"
    update_data = UpdateUserModel(
        username="updated_user"
    )
    result = await users_service.update_one(user_id, update_data)
    assert result is not None, "Updated user should not be None"

async def test_delete_one():
    users_service = UsersService(mock_database_service(), mock_id_generator_service())
    user_id = "test_user_id"
    result = await users_service.delete_one(user_id)
    assert result is None, "Delete operation should return None"
    
    # Verify that the user no longer exists
    get_result = await users_service.get_one(user_id)
    assert get_result is None, "User should be deleted and not found"
