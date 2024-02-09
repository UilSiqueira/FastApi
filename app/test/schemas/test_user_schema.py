from datetime import datetime
import pytest
from app.schemas.user import User, TokenData


async def test_user_schema():
    user = User(username="JohnDoe", password="pass#")
    assert user.model_dump() == {"username": "JohnDoe", "password": "pass#"}


async def test_user_schema_invalid_username():
    with pytest.raises(ValueError):
        User(username="JohnDoe#", password="pass#")


async def test_token_date():
    expires_at = datetime.now()
    token_data = TokenData(access_token="token test", expires_at=expires_at)

    assert token_data.model_dump() == {
        "access_token": "token test",
        "expires_at": expires_at,
    }
