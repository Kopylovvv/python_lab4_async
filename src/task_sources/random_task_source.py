import random

from src.task import Task


class RandomTaskSource:
    """
    Источник задач, генерирующий их программно.
    """

    def __init__(self, count: int = 5):
        """
        Инициализация генератора задач.

        Args:
            count: Количество генерируемых задач
        """
        self.count = count

    def get_tasks(self) -> list[Task]:
        """
        Генерация случайных задач.

        Returns:
            list[Task]: Список сгенерированных задач
        """
        tasks = []
        task_types = ["order", "notification", "stats", "check", "process"]

        for i in range(self.count):
            task_id = f"gen_{i}_{random.randint(1000, 9999)}"
            task_type = random.choice(task_types)

            # Генерация разных payload в зависимости от типа
            match task_type:
                case "order":
                    payload = {"type": "order", "order_id": random.randint(1, 1000)}
                case "notification":
                    payload = {
                        "type": "notification",
                        "user": f"user_{random.randint(1, 100)}",
                        "message": "Test notification"
                    }
                case "stats":
                    payload = {"type": "stats", "period": random.choice(["hour", "day", "week"])}
                case _:
                    payload = {"type": task_type, "value": random.random()}

            tasks.append(Task(id=task_id, payload=payload))

        return tasks
