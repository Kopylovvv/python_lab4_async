from enum import Enum


def validate_string(value):
    """Валидатор для строковых значений"""
    if not isinstance(value, str):
        raise TypeError(f"Ожидается строка, получен {type(value).__name__}")
    if not value or not value.strip():
        raise ValueError("Значение не может быть пустым")
    return value.strip()


class Priority(Enum):
    """Приоритеты задачи"""
    LOW = "низкий"
    MEDIUM = "обычный"
    HIGH = "высокий"

    def __str__(self):
        return self.value

    @classmethod
    def values(cls) -> list[str]:
        """Список всех допустимых значений"""
        return [p.value for p in cls]


def validate_priority(value):
    """Валидатор для приоритета"""
    if isinstance(value, Priority):
        return value.value

    if not isinstance(value, str):
        raise TypeError(f"Ожидается строка или Priority, получен {type(value).__name__}")

    if value not in Priority.values():
        raise ValueError(
            f"Приоритет должен быть одним из: {', '.join(Priority.values())}. "
            f"Получен: '{value}'"
        )
    return value


class Status(Enum):
    """Статусы задачи"""
    PENDING = "не начата"
    IN_PROGRESS = "в работе"
    COMPLETED = "завершена"
    CANCELLED = "отменена"
    FAILED = "провалена"

    def __str__(self):
        return self.value

    @classmethod
    def values(cls) -> list[str]:
        """Список всех допустимых значений"""
        return [s.value for s in cls]


def validate_status(value):
    """Валидатор для статуса"""
    if isinstance(value, Status):
        return value.value

    if not isinstance(value, str):
        raise TypeError(f"Ожидается строка или Status, получен {type(value).__name__}")

    if value not in Status.values():
        raise ValueError(
            f"Статус должен быть одним из: {', '.join(Status.values())}. "
            f"Получен: '{value}'"
        )
    return value
