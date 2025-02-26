from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.models import User
from app.api.schemas import UserBase


async def create_user(db: AsyncSession, user: UserBase):
    """
    Создание нового пользователя.
    """
    db_user = User(name=user.name)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_id(db: AsyncSession, user_id: int):
    """
    Получение пользователя по ID.
    """
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def update_user_balance(
    db: AsyncSession, user_id: int, new_balance: float
):
    """
    Обновление баланса пользователя.
    """
    db_user = await get_user_by_id(db, user_id)
    if db_user:
        db_user.balance = new_balance
        await db.commit()
        await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    """
    Удаление пользователя по ID.
    """
    db_user = await get_user_by_id(db, user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user
