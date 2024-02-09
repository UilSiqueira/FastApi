from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.future import select
from fastapi import status
from app.db.models import Product as ProductModel
from app.db.models import Category as CategoryModel
from app.schemas.product import Product, ProductOutput


class ProductUseCases:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def add_product(self, product: Product, category_slug: str):
        async with self.db_session as session:
            query = select(CategoryModel).filter(CategoryModel.slug == category_slug)
            result = await session.execute(query)
            category = result.scalars().unique().one_or_none()

            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No category was found with slug {category_slug}",
                )

            product_model = ProductModel(**product.model_dump())
            product_model.category_id = category.id

            session.add(product_model)
            await session.commit()

    async def update_product(self, id: int, product: Product):
        async with self.db_session as session:
            query = select(ProductModel).filter(ProductModel.id == id)
            result = await session.execute(query)
            product_on_db = result.scalars().unique().one_or_none()

            if not product_on_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No product was found with the given id",
                )

            product_on_db.name = product.name
            product_on_db.slug = product.slug
            product_on_db.price = product.price
            product_on_db.stock = product.stock

            session.add(product_on_db)
            await session.commit()

    async def delete_product(self, id: int):
        async with self.db_session as session:

            query = select(ProductModel).filter(ProductModel.id == id)
            result = await session.execute(query)
            product_on_db = result.scalars().unique().one_or_none()

            if product_on_db is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No product was found with the given id",
                )

            await session.delete(product_on_db)
            await session.commit()

    async def list_products(self, search: str = ""):
        async with self.db_session as session:
            query = select(ProductModel).filter(
                or_(
                    ProductModel.name.ilike(f"%{search}%"),
                    ProductModel.slug.ilike(f"%{search}%"),
                )
            )

            result = await session.execute(query)
            products_on_db = result.scalars().unique().all()

            products = [
                await self._serialize_product(product_on_db)
                for product_on_db in products_on_db
            ]

            return products

    async def _serialize_product(self, product_on_db: ProductModel):
        product_dict = product_on_db.__dict__
        product_dict["category"] = product_on_db.category.__dict__

        return ProductOutput(**product_dict)
