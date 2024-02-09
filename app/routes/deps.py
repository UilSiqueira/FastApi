from decouple import config
from typing import AsyncGenerator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.connection import Session as asyncSession
from app.use_cases.user import UserUseCases
from sqlalchemy.ext.asyncio import AsyncSession

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

TEST_MODE = config("TEST_MODE", default=False, cast=bool)


async def get_db_session() -> AsyncGenerator:
    try:
        session: AsyncSession = asyncSession()
        yield session
    finally:
        await session.close()


def auth(db_session: Session = Depends(get_db_session), token=Depends(oauth_scheme)):

    if TEST_MODE:
        return

    uc = UserUseCases(db_session=db_session)
    uc.verify_token(token=token)
