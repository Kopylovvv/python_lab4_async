from src.protocol import TaskSource
from src.task import Task


def validate_task_source(source) -> bool:
    """
    Валидация источника задач с проверкой метода get_tasks.

    Args:
        source: Проверяемый источник

    Returns:
        bool: True, если источник корректен

    Raises:
        TypeError: Если источник не реализует контракт
    """
    # Проверка, реализует ли объект контракт TaskSource
    if not isinstance(source, TaskSource):
        raise TypeError(f"Объект {type(source).__name__} не реализует контракт TaskSource")

    # Проверка наличия метода
    if not hasattr(source, 'get_tasks'):
        raise TypeError(f"Объект {type(source).__name__} не имеет метода get_tasks")

    # Проверка, что метод вызывается и возвращает список задач
    tasks = source.get_tasks()
    if not isinstance(tasks, list):
        raise TypeError(f"Метод get_tasks должен возвращать список, получен {type(tasks)}")

    # Проверка типов элементов
    for task in tasks:
        if not isinstance(task, Task):
            raise TypeError(f"Элемент списка должен быть Task, получен {type(task)}")
        if not isinstance(task.id, str):
            raise TypeError(f"ID задачи должен быть строкой, получен {type(task.id)}")

    return True
