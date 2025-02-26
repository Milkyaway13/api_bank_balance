from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from .config import settings


class PreBase:
    """
    Базовый класс для всех моделей, автоматически определяющий имя таблицы
    по имени класса и наследующий базовый первичный ключ.
    """

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Генерирует имя таблицы автоматически на основе имени класса.
        """
        return cls.__name__.lower()

    id: Column = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url, echo=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session():
    """
    Асинхронный контекстный менеджер для работы с сессией базы данных.
    Предоставляет сессию и закрывает её после завершения работы.

    Yields:
        AsyncSession: Асинхронная сессия для выполнения операций с БД.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
