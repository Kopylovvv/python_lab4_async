from src.task import Task


class APITaskSource:
    """
    Источник задач из API-заглушки.
    Имитирует получение задач из внешнего API.
    """

    def __init__(self, endpoint: str = "http://fake-api.example.com/tasks"):
        """
        Инициализация API-источника.

        Args:
            endpoint: URL эндпоинта API
        """
        self.endpoint = endpoint

    def get_tasks(self) -> list[Task]:
        """
        Получение задач через API.

        Returns:
            List[Task]: Список задач из API
        """
        # Эмуляция API-запроса
        api_response = {
            "status": "success",
            "data": [
                {"id": "api_001", "type": "email", "recipient": "user@example.com"},
                {"id": "api_002", "type": "report", "format": "pdf"},
                {"id": "api_003", "type": "sync", "target": "external_system"},
            ]
        }

        tasks = []
        for item in api_response["data"]:
            task_id = item["id"]
            payload = {k: v for k, v in item.items() if k != "id"}
            tasks.append(Task(id=task_id, payload=payload))

        return tasks
