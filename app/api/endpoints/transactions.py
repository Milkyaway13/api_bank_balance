from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.responses import (
    deposit_responses,
    transfer_responses,
    withdraw_responses,
)
from app.api.schemas import (
    DepositResponse,
    WithdrawResponse,
    TransferResponse,
    TransactionDeposit,
    TransactionHistoryResponse,
    TransactionTransfer,
    UserTransactionsResponse,
    WithdrawRequest,
)
from app.api.validators import (
    validate_positive_amount,
    validate_sufficient_funds,
    validate_transfer_users,
    validate_user_exists,
    validate_users_exist,
)
from app.core.db import get_async_session
from app.core.errors import ErrorMessages
from app.core.messages import Messages
from app.crud.transactions import (
    deposit_to_user,
    get_user_transactions,
    transfer_funds,
    withdraw_from_user,
)
from app.crud.users import get_user_by_id


router = APIRouter()


@router.post(
    "/deposit/{user_id}",
    response_model=DepositResponse,
    responses=deposit_responses,
)
async def deposit_funds(
    user_id: int,
    transaction: TransactionDeposit,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Пополнение баланса пользователя.
    """
    try:
        validate_positive_amount(transaction.amount)
        db_user = await deposit_to_user(db, user_id, transaction.amount)
        validate_user_exists(db_user)
        await db.commit()
        return DepositResponse(
            message=(
                f"{Messages.SUCCESS_DEPOSIT_MESSAGE.value} - {db_user.balance}"
            )
            )

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessages.DATABASE_ERROR_MESSAGE,
        )

    except HTTPException as e:
        raise e

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessages.UNDEFINED_ERROR_MESSAGE,
        )


@router.post(
    "/withdraw/{user_id}",
    response_model=WithdrawResponse,
    responses=withdraw_responses,
)
async def withdraw_funds(
    user_id: int,
    transaction: WithdrawRequest,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Списание средств с баланса пользователя.
    """
    try:
        validate_positive_amount(transaction.amount)
        db_user = await get_user_by_id(db, user_id)
        validate_user_exists(db_user)
        validate_sufficient_funds(db_user.balance, transaction.amount)
        db_user = await withdraw_from_user(db, user_id, transaction.amount)
        await db.commit()
        return WithdrawResponse(
            message=(
                f"{Messages.SUCCESS_WITHDRAW_MESSAGE.value}-{db_user.balance}"
            )
            )

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessages.DATABASE_ERROR_MESSAGE,
        )

    except HTTPException as e:
        raise e

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessages.UNDEFINED_ERROR_MESSAGE,
        )


@router.post(
    "/transfer", response_model=TransferResponse, responses=transfer_responses
)
async def transfer_funds_between_users(
    transfer: TransactionTransfer,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Перевод средств между пользователями.
    """
    try:
        validate_positive_amount(transfer.amount)
        validate_transfer_users(transfer.from_user_id, transfer.to_user_id)
        from_user = await get_user_by_id(db, transfer.from_user_id)
        to_user = await get_user_by_id(db, transfer.to_user_id)
        validate_users_exist(from_user, to_user)
        validate_sufficient_funds(from_user.balance, transfer.amount)
        await transfer_funds(
            db, transfer.from_user_id, transfer.to_user_id, transfer.amount
        )
        await db.commit()

        return TransferResponse(
            message=f"{Messages.SUCCESS_TRANSFER_MESSAGE.value}"
            )

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessages.DATABASE_ERROR_MESSAGE,
        )

    except HTTPException as e:
        raise e

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessages.UNDEFINED_ERROR_MESSAGE,
        )


@router.get("/{user_id}/history", response_model=UserTransactionsResponse)
async def read_user_transactions(
    user_id: int, db: AsyncSession = Depends(get_async_session)
):
    """
    Получение истории операций по пользователю.
    """
    try:
        db_user = await get_user_by_id(db, user_id)
        validate_user_exists(db_user)
        transactions = await get_user_transactions(db, user_id)
        serialized_transactions = [
            TransactionHistoryResponse(
                id=transaction.id,
                amount=transaction.amount,
                type=transaction.type,
                created_at=transaction.created_at,
            )
            for transaction in transactions
        ]
        return UserTransactionsResponse(
            user_id=user_id, transactions=serialized_transactions
        )

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
