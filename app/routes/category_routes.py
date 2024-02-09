from typing import List
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.schemas.category import Category, CategoryOutput
from app.routes.deps import get_db_session, auth
from app.use_cases.category import CategoryUseCases


router = APIRouter(prefix="/category", tags=["Category"], dependencies=[Depends(auth)])


@router.post("/add", status_code=status.HTTP_201_CREATED, description="Add new category")
async def add_category(category: Category, db_session: Session = Depends(get_db_session)):

    uc = CategoryUseCases(db_session=db_session)
    await uc.add_category(category=category)

    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/list", response_model=List[CategoryOutput], description="List categories")
async def list_categories(db_session: Session = Depends(get_db_session)):

    uc = CategoryUseCases(db_session=db_session)
    response = await uc.list_categories()

    return response


@router.delete("/delete/{id}", description="Delete category")
async def delete_category(id: int, db_session: Session = Depends(get_db_session)):
    uc = CategoryUseCases(db_session=db_session)
    await uc.delete_category(id=id)

    return Response(status_code=status.HTTP_200_OK)
