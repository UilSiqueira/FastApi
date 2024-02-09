import pytest
from app.use_cases.category import CategoryUseCases
from app.db.models import Category as CategoryModel
from app.schemas.category import Category, CategoryOutput
from fastapi.exceptions import HTTPException

from sqlalchemy.future import select

from app.test.deps import db_session, categories_on_db, delete_categories_on_db

# from fastapi_pagination import Page


async def test_add_category_uc(db_session=db_session):

    category = Category(name="Clothes", slug="clothes")

    async for session in db_session():
        uc = CategoryUseCases(session)

        await uc.add_category(category=category)

        categories = await categories_on_db(session)

        len_categories = len(categories)
        category_name = categories[0].name
        category_slug = categories[0].slug

        await delete_categories_on_db(session)

    assert len_categories == 2, \
        f"Result: {len(categories)}, Expected: {2}"
    assert (category_name == "Clothes"), \
        f"Result: {categories[0].name}, Expected: {'Clothes'}"
    assert (category_slug == "clothes"), \
        f"Result: {categories[0].slug}, Expected: {'clothes'}"


async def test_list_categories_uc(db_session=db_session):
    async for session in db_session():
        listed_categories = await categories_on_db(session)

        uc = CategoryUseCases(session)
        categories = await uc.list_categories()

        len_categories = len(listed_categories)
        categories_id = listed_categories[0].id
        categoried_name = listed_categories[0].name
        categories_slug = listed_categories[0].slug

        await delete_categories_on_db(session)

    assert (len(categories) == len_categories), \
        f"Result: {len(categories)}, Expected: {len_categories}"
    assert type(categories[0]) is CategoryOutput
    assert categories[0].id == categories_id, \
        f"Result: {categories[0].id}, Expected: {categories_id}"
    assert categories[0].name == categoried_name, \
        f"Result: {categories[0].name}, Expected: {categoried_name}"
    assert categories[0].slug == categories_slug, \
        f"Result: {categories[0].slug}, Expected: {categories_slug}"


async def test_delete_category(db_session=db_session):
    async for session in db_session():

        category_model = CategoryModel(name="Clothes", slug="clothes")
        session.add(category_model)
        await session.commit()

        uc = CategoryUseCases(session)
        await uc.delete_category(id=category_model.id)

        query = select(CategoryModel)
        result = await session.execute(query)
        category_model = result.scalars().unique().all()
    assert len(category_model) == 0, \
        f"Result: {len(category_model)}, Expected: {0}"


async def test_delete_category_non_exist(db_session=db_session):
    async for session in db_session():
        uc = CategoryUseCases(session)
        with pytest.raises(HTTPException):
            await uc.delete_category(id=1)
