from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.models import User
from app.core.errors import ErrorMessages


def validate_user_exists(user: User) -> None:
    """
    Проверяет, существует ли пользователь.
    """
    if user is None:
        raise HTTPException(
            status_code=404, detail=ErrorMessages.USER_NOT_FOUND
        )


async def validate_user_does_not_exist(db: AsyncSession, name: str) -> None:
    """
    Проверяет, что пользователь с таким именем не существует.
    """
    result = await db.execute(select(User).filter(User.name == name))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ErrorMessages.USER_ALREADY_EXISTS,
        )


def validate_positive_amount(amount: float) -> None:
    """
    Проверяет, что сумма положительная.
    """
    if amount <= 0:
        raise HTTPException(
            status_code=400, detail=ErrorMessages.INVALID_AMOUNT
        )


def validate_sufficient_funds(user_balance: float, amount: float) -> None:
    """
    Проверяет, что на балансе достаточно средств.
    """
    if user_balance < amount:
        raise HTTPException(
            status_code=400, detail=ErrorMessages.INSUFFICIENT_FUNDS
        )


def validate_transfer_users(from_user_id: int, to_user_id: int) -> None:
    """
    Проверяет, что перевод выполняется между разными пользователями.
    """
    if from_user_id == to_user_id:
        raise HTTPException(
            status_code=400, detail=ErrorMessages.TRANSFER_SAME_USER
        )


def validate_users_exist(from_user: User, to_user: User) -> None:
    """
    Проверяет, что оба пользователя существуют.
    """
    if from_user and not to_user:
        raise HTTPException(
            status_code=404, detail=ErrorMessages.USER_RECIPIENT_NOT_FOUND
        )

    if not from_user and to_user:
        raise HTTPException(
            status_code=404, detail=ErrorMessages.USER_SENDER_NOT_FOUND
        )
