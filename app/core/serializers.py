from datetime import datetime
from decimal import Decimal
from typing import Any, Dict


def serialize_model(model_instance: Any) -> Dict[str, Any]:
    """
    Сериализует объект SQLAlchemy в словарь.
    """
    result = {}
    for column in model_instance.__table__.columns:
        value = getattr(model_instance, column.name)
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, Decimal):
            value = float(value)
        result[column.name] = value
    return result
