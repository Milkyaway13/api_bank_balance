from fastapi import APIRouter

from app.api.endpoints import transactions, users

router = APIRouter()


router.include_router(users.router, prefix="/users", tags=("users",))
router.include_router(
    transactions.router, prefix="/transactions", tags=("transactions",)
)
