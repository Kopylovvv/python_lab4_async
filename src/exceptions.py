class TaskValidationError(Exception):
    """Базовое исключение для ошибок валидации задачи"""
    pass


class InvalidTaskStateError(TaskValidationError):
    """Исключение при попытке установить некорректное состояние задачи"""
    pass
