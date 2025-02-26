from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.models import Transaction, TransactionType
from app.api.schemas import TransactionCreate
from app.crud.users import get_user_by_id


async def create_transaction(db: AsyncSession, transaction: TransactionCreate):
    """
    Создание новой транзакции.
    """
    db_transaction = Transaction(
        user_id=transaction.user_id,
        amount=transaction.amount,
        type=transaction.type,
    )
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction


async def get_transaction_by_id(db: AsyncSession, transaction_id: int):
    """
    Получение транзакции по ID.
    """
    result = await db.execute(
        select(Transaction).filter(Transaction.id == transaction_id)
    )
    return result.scalars().first()


async def get_user_transactions(db: AsyncSession, user_id: int):
    """
    Получение всех транзакций пользователя.
    """
    result = await db.execute(
        select(Transaction).filter(Transaction.user_id == user_id)
    )
    return result.scalars().all()


async def deposit_to_user(db: AsyncSession, user_id: int, amount: float):
    """
    Пополнение баланса пользователя.
    """
    db_user = await get_user_by_id(db, user_id)
    if db_user:
        db_user.balance += amount
        await create_transaction(
            db,
            TransactionCreate(
                user_id=user_id, amount=amount, type=TransactionType.DEPOSIT
            ),
        )
        await db.commit()
        await db.refresh(db_user)
    return db_user


async def withdraw_from_user(db: AsyncSession, user_id: int, amount: float):
    """
    Списание средств с баланса пользователя.
    """
    db_user = await get_user_by_id(db, user_id)
    if db_user:
        db_user.balance -= amount
        await create_transaction(
            db,
            TransactionCreate(
                user_id=user_id, amount=amount, type=TransactionType.WITHDRAW
            ),
        )
        await db.commit()
        await db.refresh(db_user)
    return db_user


async def transfer_funds(
    db: AsyncSession, from_user_id: int, to_user_id: int, amount: float
):
    """
    Перевод средств между пользователями.
    """
    from_user = await get_user_by_id(db, from_user_id)
    to_user = await get_user_by_id(db, to_user_id)

    if not from_user or not to_user:
        return None

    if from_user.balance < amount:
        return "insufficient_funds"

    from_user.balance -= amount
    to_user.balance += amount

    await create_transaction(
        db,
        TransactionCreate(
            user_id=from_user_id, amount=amount, type=TransactionType.TRANSFER
        ),
    )
    await create_transaction(
        db,
        TransactionCreate(
            user_id=to_user_id, amount=amount, type=TransactionType.TRANSFER
        ),
    )

    await db.commit()
    await db.refresh(from_user)
    await db.refresh(to_user)
