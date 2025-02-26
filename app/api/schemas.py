from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class TransactionType(str, Enum):
    """
    Перечисление для типов транзакций.

    Атрибуты:
        DEPOSIT: Тип транзакции "пополнение".
        WITHDRAW: Тип транзакции "списание".
        TRANSFER: Тип транзакции "перевод".
    """
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"


class UserBase(BaseModel):
    """
    Базовая схема для пользователя.

    Атрибуты:
        name: Имя пользователя.
    """
    name: str


class TransactionBase(BaseModel):
    """
    Базовая схема для транзакции.

    Атрибуты:
        amount: Сумма транзакции.
        type: Тип транзакции (пополнение, списание, перевод).
    """
    amount: float
    type: TransactionType


class TransactionCreate(TransactionBase):
    """
    Схема для создания транзакции.

    Атрибуты:
        user_id: Идентификатор пользователя, связанного с транзакцией.
    """
    user_id: int


class TransactionDeposit(BaseModel):
    """
    Схема для пополнения баланса.

    Атрибуты:
        amount: Сумма для пополнения.
    """
    amount: float = Field(example=100.0)


class TransactionHistoryResponse(BaseModel):
    """
    Схема для отображения истории транзакций.

    Атрибуты:
        id: Уникальный идентификатор транзакции.
        amount: Сумма транзакции.
        type: Тип транзакции (пополнение, списание, перевод).
        created_at: Дата и время создания транзакции.
    """
    id: int = Field(example=1)
    amount: float = Field(example=100.0)
    type: str = Field(example="deposit")
    created_at: datetime


class TransactionTransfer(BaseModel):
    """
    Схема для перевода средств между пользователями.

    Атрибуты:
        from_user_id: Идентификатор пользователя-отправителя.
        to_user_id: Идентификатор пользователя-получателя средства.
        amount: Сумма перевода.
    """
    from_user_id: int = 1
    to_user_id: int = 2
    amount: float = 100


class UserResponse(UserBase):
    """
    Схема для отображения информации о пользователе.

    Атрибуты:
        id: Уникальный идентификатор пользователя.
        balance: Текущий баланс пользователя.
        created_at: Дата и время создания пользователя.
    """
    id: int = Field(example=1)
    balance: float = Field(example=100)
    created_at: datetime

    class Config:
        from_attributes = True


class UserTransactionsResponse(BaseModel):
    """
    Схема для отображения списка транзакций пользователя.

    Атрибуты:
        user_id: Идентификатор пользователя.
        transactions: Список транзакций пользователя.
    """
    user_id: int = 1
    transactions: List[TransactionHistoryResponse]


class MessageResponse(BaseModel):
    """
    Базовая схема для ответа с сообщением.

    Атрибуты:
        message: Текст сообщения.
    """
    message: str


class WithdrawResponse(MessageResponse):
    """
    Схема для ответа на запрос списания средств.

    Наследует:
        MessageResponse: Базовая схема с сообщением.
    """
    pass


class DepositResponse(MessageResponse):
    """
    Схема для ответа на запрос пополнения средств.

    Наследует:
        MessageResponse: Базовая схема с сообщением.
    """
    pass


class TransferResponse(MessageResponse):
    """
    Схема для ответа на запрос перевода средств.

    Наследует:
        MessageResponse: Базовая схема с сообщением.
    """
    pass


class WithdrawRequest(BaseModel):
    """
    Схема для запроса списания средств.

    Атрибуты:
        amount: Сумма для списания.
    """
    amount: float = Field(example=100.0)
