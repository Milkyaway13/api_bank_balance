from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import UserBase, UserResponse
from app.api.validators import (
    validate_user_does_not_exist,
    validate_user_exists,
)
from app.core.db import get_async_session
from app.core.errors import ErrorMessages
from app.core.serializers import serialize_model
from app.crud.users import create_user, get_user_by_id

router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_new_user(
    user: UserBase, db: AsyncSession = Depends(get_async_session)
):
    """
    Создание нового пользователя.
    """
    try:
        await validate_user_does_not_exist(db, user.name)
        db_user = await create_user(db, user)
        user_data = serialize_model(db_user)
        await db.commit()
        return UserResponse(**user_data)

    except HTTPException as e:
        raise e

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessages.DATABASE_ERROR_MESSAGE,
        )

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Неизвестная ошибка",
        )


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int, db: AsyncSession = Depends(get_async_session)
):
    """
    Получение информации о пользователе по ID.
    """
    try:
        db_user = await get_user_by_id(db, user_id)
        validate_user_exists(db_user)
        user_data = serialize_model(db_user)
        return UserResponse(**user_data)

    except HTTPException as e:
        raise e

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessages.DATABASE_ERROR_MESSAGE,
        )

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessages.UNDEFINED_ERROR_MESSAGE,
        )
