from fastapi import status
from app.main import app
import httpx
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.db.models import User as UserModel
from app.test.deps import db_session, user_on_db

# constants
HTTP_201_CREATED = status.HTTP_201_CREATED
HTTP_404_NOT_FOUND = status.HTTP_404_NOT_FOUND
HTTP_200_OK = status.HTTP_200_OK
HTTP_400_BAD_REQUEST = status.HTTP_400_BAD_REQUEST
HTTP_401_UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED

BASE_URL = "http://testserver"
LOGIN_ENDPOINT = "/user/login"

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Bearer token",
}
PASSWORD = "pass#"

crypt_context = CryptContext(schemes=["sha256_crypt"])


async def test_register_user_route(db_session=db_session):
    body = {"username": "JohnDoe", "password": PASSWORD}

    async for session in db_session():
        async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
            response = await client.post("/user/register", json=body)

        assert (response.status_code == HTTP_201_CREATED), \
            (f"Result: {response.status_code}", "Expected: {HTTP_201_CREATED}")

        query = select(UserModel)
        result = await session.execute(query)
        user_on_db = result.scalars().unique().one_or_none()

        await session.delete(user_on_db)
        await session.commit()

    assert (user_on_db is not None), \
        f"Result: {user_on_db is not None},  Expected: User on db is True"


async def test_register_user_route_user_already_exists(db_session=db_session):
    async for session in db_session():
        user = await user_on_db(session)

        body = {"username": user.username, "password": PASSWORD}

        async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
            response = await client.post("/user/register", json=body)

            await session.delete(user)
            await session.commit()

        assert (response.status_code == HTTP_400_BAD_REQUEST), \
            f"Result: {response.status_code}, Expected: {HTTP_400_BAD_REQUEST}"


async def test_user_login_route(db_session=db_session):
    async for session in db_session():
        user = await user_on_db(session)
        username = user.username

        body = {"username": username, "password": PASSWORD}

        async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
            response = await client.post(LOGIN_ENDPOINT, data=body, headers=HEADERS)

            data = response.json()

            await session.delete(user)
            await session.commit()

        assert (response.status_code == HTTP_200_OK), \
            f"Result: {response.status_code}, Expected: {HTTP_200_OK}"
        assert "access_token" in data
        assert "expires_at" in data


async def test_user_login_route_invalid_username():
    body = {"username": "Invalid", "password": PASSWORD}

    async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post(LOGIN_ENDPOINT, data=body, headers=HEADERS)

    assert (response.status_code == HTTP_401_UNAUTHORIZED), \
        f"Result: {response.status_code}, Expected: {HTTP_401_UNAUTHORIZED}"


async def test_user_login_route_invalid_password(db_session=db_session):
    async for session in db_session():
        user = await user_on_db(session)
        username = user.username

        body = {"username": username, "password": "invalid"}

        async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
            response = await client.post(LOGIN_ENDPOINT, data=body, headers=HEADERS)

            await session.delete(user)
            await session.commit()

    assert (
        response.status_code == HTTP_401_UNAUTHORIZED), \
        f"Result: {response.status_code}, Expected: {HTTP_401_UNAUTHORIZED}"
