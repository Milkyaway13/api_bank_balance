from app.core.messages import Messages

transfer_responses = {
    200: {
        "description": "Успешный перевод средств",
        "content": {
            "application/json": {
                "example": {
                    "message": f"{Messages.SUCCESS_TRANSFER_MESSAGE.value}"
                }
            }
        },
    },
}
deposit_responses = {
    200: {
        "description": "Успешное пополнение счета",
        "content": {
            "application/json": {
                "example": {
                    "message": (
                        f"{Messages.SUCCESS_DEPOSIT_MESSAGE.value} - 100"
                    )
                }
            }
        },
    },
}
withdraw_responses = {
    200: {
        "description": "Успешное списание перевод средств",
        "content": {
            "application/json": {
                "example": {
                    "message": (
                        f"{Messages.SUCCESS_WITHDRAW_MESSAGE.value} - 50"
                    )
                }
            }
        },
    },
}
