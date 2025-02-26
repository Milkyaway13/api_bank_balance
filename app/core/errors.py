from enum import Enum


class ErrorMessages(str, Enum):
    """
    Класс для управления стандартными сообщениями об ошибках.

    Атрибуты:
    USER_NOT_FOUND: Возвращается, когда запрашиваемый пользователь не найден.
    USER_ALREADY_EXISTS: Возвращается, когда пользователь уже существует.
    INSUFFICIENT_FUNDS: Возвращается,когда у пользователя недостаточно средств.
    INVALID_AMOUNT: Возвращается, когда сумма транзакции не положительная.
    TRANSFER_SAME_USER: Возвращается, когда пользователь делает перевод себе.
    """

    USER_NOT_FOUND = "Пользователь не найден"
    USER_SENDER_NOT_FOUND = "Пользоваель-отправитель не найден"
    USER_RECIPIENT_NOT_FOUND = "Пользователь-получатель не найден"
    USER_ALREADY_EXISTS = "Пользователь уже существует"
    INSUFFICIENT_FUNDS = "Недостаточно средств на балансе"
    INVALID_AMOUNT = "Сумма должна быть положительной"
    TRANSFER_SAME_USER = "Нельзя переводить средства самому себе"
    DATABASE_ERROR_MESSAGE = "Ошибка базы данных."
    UNDEFINED_ERROR_MESSAGE = "Неизвестная ошибка."
