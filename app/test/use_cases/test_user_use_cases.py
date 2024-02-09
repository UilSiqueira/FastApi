import pytest
from decouple import config
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from fastapi.exceptions import HTTPException
from app.schemas.user import User
from app.db.models import User as UserModel
from app.use_cases.user import UserUseCases

from sqlalchemy.future import select

from app.test.deps import db_session, user_on_db, delete_user_on_db


crypt_context = CryptContext(schemes=["sha256_crypt"])

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")


async def test_register_user(db_session=db_session):
    async for session in db_session():
        user = User(username="JohnDoe", password="pass#")

        uc = UserUseCases(session)
        await uc.register_user(user=user)

        query = select(UserModel)
        result = await session.execute(query)
        user_on_db = result.scalars().unique().first()

        assert (user_on_db is not None), \
            f"Result: { user_on_db is not None}, Expected: {True}"
        assert user_on_db.username == user.username
        assert crypt_context.verify(user.password, user_on_db.password)

        await delete_user_on_db(session, user_on_db)


async def test_register_user_username_already_exists(db_session=db_session):
    async for session in db_session():

        user_on_db = UserModel(username="JohnDoe", password=crypt_context.hash("pass#"))

        session.add(user_on_db)
        await session.commit()

        uc = UserUseCases(session)

        user = User(username="JohnDoe", password=crypt_context.hash("pass#"))

        with pytest.raises(HTTPException):
            await uc.register_user(user=user)

        await delete_user_on_db(session, user_on_db)


async def teste_user_login(db_session=db_session):
    async for session in db_session():
        user_from_db = await user_on_db(session)
        uc = UserUseCases(session)

        user = User(username=user_from_db.username, password="pass#")

        await uc.user_login(user=user, expires_in=30)
        token_data = await uc.user_login(user=user, expires_in=30)

        await delete_user_on_db(session, user_from_db)

        assert token_data.expires_at < datetime.utcnow() + timedelta(31)


async def test_user_login_invalid_username(db_session=db_session):
    async for session in db_session():
        uc = UserUseCases(session)

        user = User(username="Invalid", password="pass#")

        with pytest.raises(HTTPException):
            await uc.user_login(user=user, expires_in=30)


async def test_user_login_invalid_password(db_session=db_session):
    async for session in db_session():
        user_from_db = await user_on_db(session)
        uc = UserUseCases(session)

        user = User(username=user_from_db.username, password="Invalid")

        with pytest.raises(HTTPException):
            await uc.user_login(user=user, expires_in=30)

        await delete_user_on_db(session, user_from_db)


async def test_verify_token(db_session=db_session):
    async for session in db_session():
        user_from_db = await user_on_db(session)
        uc = UserUseCases(session)

        data = {
            "sub": user_from_db.username,
            "exp": datetime.utcnow() + timedelta(minutes=30),
        }

        access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

        await uc.verify_token(token=access_token)

        await delete_user_on_db(session, user_from_db)


async def test_verify_token_expired(db_session=db_session):
    async for session in db_session():
        user_from_db = await user_on_db(session)
        uc = UserUseCases(session)

        data = {
            "sub": user_from_db.username,
            "exp": datetime.utcnow() - timedelta(minutes=30),
        }

        access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

        with pytest.raises(HTTPException):
            await uc.verify_token(token=access_token)

        await delete_user_on_db(session, user_from_db)
