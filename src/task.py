import time
from typing import Optional, Any

from src.descriptors import ValidatedAttribute
from src.validators import validate_string, validate_priority, validate_status, Status, Priority
from src.exceptions import TaskValidationError, InvalidTaskStateError


class Task:
    """
    Модель задачи

    Data descriptors (всегда валидируются):
        id: Уникальный идентификатор (нельзя изменить после создания)
        description: Описание задачи (можно изменить до начала выполнения)
        priority: Приоритет задачи (можно изменить до начала выполнения)
        status: Текущий статус задачи

    Атрибуты (прямое хранение):
        _created_at: Время создания (неизменяемо)
        payload: Произвольные данные задачи (из первой лабы)

    Вычисляемые свойства (property):
        created_at: Время создания (только для чтения)
        age: Возраст задачи в секундах
        can_edit: Можно ли редактировать задачу
        can_start: Можно ли запустить задачу
        is_active: Активна ли задача (в работе или ожидает)
        is_finished: Завершена ли задача (любым исходом)
        priority_enum: Приоритет как Enum (удобно для сравнения)
        status_enum: Статус как Enum (удобно для сравнения)
    """

    # Data descriptors для валидации
    id = ValidatedAttribute(validate_string)
    description = ValidatedAttribute(validate_string)
    priority = ValidatedAttribute(validate_priority)
    status = ValidatedAttribute(validate_status)

    def __init__(self, id: str, payload: Any):
        """
        Инициализация задачи

        Args:
            id: Уникальный идентификатор (нельзя изменить потом)
            payload: Произвольные данные задачи

        Raises:
            TaskValidationError: При некорректных значениях
        """
        try:
            # Устанавливаем значения через дескрипторы (валидация происходит здесь)
            self.id = id

            self.payload = payload

            if 'description' in payload:
                self.description = payload['description']
            else:
                self.description = f"Задача {id}"

            if 'priority' in payload:
                self.priority = payload['priority']
            else:
                self.priority = "обычный"

            # status: всегда начинается с "не начата"
            self.status = Status.PENDING.value

            # Приватные атрибуты
            self._created_at = time.time()


        except (TypeError, ValueError) as e:
            raise TaskValidationError(f"Ошибка создания задачи: {e}") from e

    # Свойства

    @property
    def created_at(self) -> float:
        """Время создания"""
        return self._created_at

    @property
    def priority_enum(self) -> Priority:
        """Приоритет как Enum"""
        for p in Priority:
            if p.value == self.priority:
                return p
        return Priority.MEDIUM

    @property
    def status_enum(self) -> Status:
        """Статус как Enum"""
        for s in Status:
            if s.value == self.status:
                return s
        return Status.PENDING

    # Вычисляемые свойства

    @property
    def age(self) -> float:
        """Возраст задачи в секундах"""
        return time.time() - self._created_at

    @property
    def can_edit(self) -> bool:
        """Можно ли редактировать задачу (только пока не начата)"""
        return self.status_enum == Status.PENDING

    @property
    def can_start(self) -> bool:
        """Можно ли запустить задачу (только если не начата)"""
        return self.status_enum == Status.PENDING

    @property
    def is_active(self) -> bool:
        """Активна ли задача (не завершена, не отменена и не провалена)"""
        return self.status_enum in [Status.PENDING, Status.IN_PROGRESS]

    @property
    def is_finished(self) -> bool:
        """Завершена ли задача (любым исходом)"""
        return self.status_enum in [Status.COMPLETED, Status.CANCELLED, Status.FAILED]

    # --- Методы для изменения атрибутов с проверками ---

    def edit(self, description: Optional[str] = None, priority: Optional[str] = None) -> None:
        """
        Изменить описание или приоритет задачи
        Можно менять только пока задача не начата

        Args:
            description: Новое описание (если None - не меняется)
            priority: Новый приоритет (строка или объект Priority)

        Raises:
            InvalidTaskStateError: Если задача уже начата
        """
        if not self.can_edit:
            raise InvalidTaskStateError(
                f"Нельзя редактировать задачу в статусе '{self.status}'. "
                f"Редактирование возможно только для задач со статусом 'не начата'"
            )

        if description is not None and description != self.description:
            self.description = description

        if priority is not None:
            priority_value = priority.value if isinstance(priority, Priority) else priority
            if priority_value != self.priority:
                self.priority = priority_value

    # --- Методы изменения статуса ---

    def start(self) -> None:
        """Начать выполнение задачи"""
        if not self.can_start:
            raise InvalidTaskStateError(
                f"Нельзя запустить задачу со статусом '{self.status}'. "
                f"Ожидался статус 'не начата'"
            )
        self.status = Status.IN_PROGRESS.value

    def complete(self) -> None:
        """Завершить задачу успешно"""
        if self.status_enum != Status.IN_PROGRESS:
            raise InvalidTaskStateError(
                f"Нельзя завершить задачу со статусом '{self.status}'. "
                f"Завершить можно только задачу 'в работе'"
            )
        self.status = Status.COMPLETED.value

    def fail(self) -> None:
        """Отметить задачу как проваленную"""
        if self.status_enum not in [Status.PENDING, Status.IN_PROGRESS]:
            raise InvalidTaskStateError(
                f"Нельзя провалить задачу со статусом '{self.status}'"
            )
        self.status = Status.FAILED.value

    def cancel(self) -> None:
        """Отменить задачу."""
        if self.status_enum not in [Status.PENDING, Status.IN_PROGRESS]:
            raise InvalidTaskStateError(
                f"Нельзя отменить задачу со статусом '{self.status}'"
            )
        self.status = Status.CANCELLED.value

    def get_info(self) -> dict[str, Any]:
        """Получить полную информацию о задаче."""
        return {
            'id': self.id,
            'description': self.description,
            'priority': self.priority,
            'priority_enum': self.priority_enum.name,
            'status': self.status,
            'status_enum': self.status_enum.name,
            'created_at': self._created_at,
            'age': self.age,
            'can_edit': self.can_edit,
            'can_start': self.can_start,
            'is_active': self.is_active,
            'is_finished': self.is_finished,
            'payload': self.payload,
        }

    # --- Магические методы ---

    def __str__(self) -> str:
        return (f"Задача [{self.id}]:\n"
                f"Описание: {self.description}\n"
                f"Статус: {self.status}\n"
                f"Приоритет: {self.priority}\n"
                f"Возраст: {self.age:.1f} сек\n"
                f"payload: {self.payload}")
