import pytest
from app.schemas.category import Category


async def test_category_schema():
    category = Category(
        name="Clothes",
        slug="clothes",
    )

    assert category.model_dump() == {"name": "Clothes", "slug": "clothes"}


async def test_category_schema_invalid_slug():
    with pytest.raises(ValueError):
        Category(
            name="Clothes",
            slug="labour clothes",
        )
