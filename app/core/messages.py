from enum import Enum


class Messages(str, Enum):
    """
    Класс для управления стандартными сообщениями об ошибках.

    Атрибуты:
    SUCCESS_TRANSFER_MESSAGE: Сообщение об успешном переводе средств.
    SUCCESS_WITHDRAW_MESSAGE: Сообщение об успешном списании средств.
    SUCCESS_DEPOSIT_MESSAGE: Сообщение об успешном пополнении баланса.
    """

    SUCCESS_TRANSFER_MESSAGE = "Перевод успешно выполнен."
    SUCCESS_WITHDRAW_MESSAGE = "Средства успешно списаны. Текущий баланс"
    SUCCESS_DEPOSIT_MESSAGE = "Баланс успешно пополнен. Текущий баланс"
