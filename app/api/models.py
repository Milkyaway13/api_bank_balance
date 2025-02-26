from enum import Enum

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db import Base


class User(Base):
    """
    Представление пользователя в базе данных.

    Attributes:
        id (int): Уникальный идентификатор пользователя.
        name (str): Имя пользователя.
        balance (float): Баланс пользователя.
        created_at (DateTime): Время создания записи пользователя.
        transactions (relationship): Связь с транзакциями пользователя.
    """

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, index=True)
    balance: float = Column(Float, default=0.0)
    created_at: DateTime = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    transactions = relationship(
        "Transaction", order_by="Transaction.id", back_populates="user"
    )


class TransactionType(str, Enum):
    """
    Типы транзакций, поддерживаемые системой.
    """

    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"


class Transaction(Base):
    """
    Представление транзакции в базе данных.

    Attributes:
        id (int): Уникальный идентификатор транзакции.
        user_id (int): Внешний ключ для связи с пользователем.
        amount (float): Сумма транзакции.
        type (TransactionType): Тип транзакции.
        created_at (DateTime): Время создания записи транзакции.
        user (relationship): Обратная связь с пользователем.
    """

    __tablename__ = "transactions"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    amount: float = Column(Float)
    type: TransactionType = Column(SQLEnum(TransactionType))
    created_at: DateTime = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    user = relationship("User", back_populates="transactions")
