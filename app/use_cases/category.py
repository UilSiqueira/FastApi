# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Category as CategoryModel
from app.schemas.category import Category, CategoryOutput
from fastapi.exceptions import HTTPException
from fastapi import status


class CategoryUseCases:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def add_category(self, category: Category):
        async with self.db_session as session:
            category_model = CategoryModel(**category.model_dump())
            session.add(category_model)
            await session.commit()

    async def list_categories(self):
        async with self.db_session as session:
            query = select(CategoryModel)
            result = await session.execute(query)
            categories_on_db = result.scalars().unique().all()

            categories_output = [
                await self.serialize_category(category_model)
                for category_model in categories_on_db
            ]

            return categories_output

    async def delete_category(self, id: int):
        async with self.db_session as session:
            query = select(CategoryModel).filter(CategoryModel.id == id)
            result = await session.execute(query)
            category_model = result.scalars().unique().one_or_none()

            if not category_model:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
                )

            await session.delete(category_model)
            await session.commit()

    async def serialize_category(self, category_model: CategoryModel):
        return CategoryOutput(**category_model.__dict__)
