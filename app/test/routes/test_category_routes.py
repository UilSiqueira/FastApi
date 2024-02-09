from fastapi import status
from app.main import app
import httpx
from sqlalchemy.future import select

from app.db.models import Category as CategoryModel
from app.test.deps import db_session, categories_on_db, delete_categories_on_db

# constants
HTTP_201_CREATED = status.HTTP_201_CREATED
HTTP_404_NOT_FOUND = status.HTTP_404_NOT_FOUND
HTTP_200_OK = status.HTTP_200_OK

BASE_URL = "http://testserver"

headers = {"Authorization": "Bearer token"}


async def test_add_category_route(db_session=db_session):

    body = {"name": "Clothes", "slug": "clothes"}

    async for session in db_session():
        async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
            response = await client.post("/category/add", json=body, headers=headers)

        query = select(CategoryModel)
        result = await session.execute(query)
        categories_on_db = result.scalars().unique().all()

        len_categories = len(categories_on_db)

        await delete_categories_on_db(session)

    assert (response.status_code == HTTP_201_CREATED), \
        f"Result: {response.status_code}, Expected: {HTTP_201_CREATED}"
    assert len_categories == 1, \
        f"Result: {len_categories}, Expected: {1}"


async def test_list_categories_route(db_session=db_session):
    async for session in db_session():
        categories = await categories_on_db(session)

        async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
            response = await client.get("/category/list", headers=headers)

        data = response.json()
        categories_slug = categories[0].slug

        await delete_categories_on_db(session)

    assert (response.status_code == HTTP_200_OK), \
        f"Result: {response.status_code}, Expected: {HTTP_200_OK}"
    assert len(data) == 2, \
        f"Result: {len(data)}, Expected: {2}"
    assert (data[0]["slug"] == categories_slug), \
        f"Result: {data[0]['slug']}, Expected: {categories_slug}"


async def test_delete_category_route(db_session=db_session):
    async for session in db_session():
        category_model = CategoryModel(name="Glasses", slug="glasses")

        session.add(category_model)
        await session.commit()

        async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
            response = await client.delete(
                f"/category/delete/{category_model.id}", headers=headers
            )

        query = select(CategoryModel).filter(CategoryModel.id == category_model.id)
        result = await session.execute(query)
        category_model = result.scalars().unique().one_or_none()

    assert (response.status_code == HTTP_200_OK), \
        f"Result: {response.status_code}, Expected: {HTTP_200_OK}"
    assert category_model is None, f"{type(category_model)}"
