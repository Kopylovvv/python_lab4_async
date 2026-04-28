import json

from src.task import Task


class FileTaskSource:
    """
    Источник задач из файла.
    чтение задач из JSON-файла.
    """

    def __init__(self, file_path: str):
        """
        Инициализация источника.

        Args:
            file_path: Путь к файлу с задачами
        """
        self.file_path = file_path

    def get_tasks(self) -> list[Task]:
        """
        Чтение задач из файла.

        Returns:
            list[Task]: Список задач из файла
        """
        # Чтение из реального файла
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                tasks_data = json.load(file)

                # Проверка, что данные - это список
                if not isinstance(tasks_data, list):
                    print(f"Ошибка: файл {self.file_path} должен содержать список задач")
                    return []

                # Преобразование данных в задачи
                tasks = []
                for task in tasks_data:
                    if "id" not in task:
                        print(f"Пропущен элемент: {task} - отсутствует поле 'id'")
                        continue

                    task_id = task["id"]
                    payload = {k: v for k, v in task.items() if k != "id"}
                    tasks.append(Task(task_id, payload))

                return tasks

        except FileNotFoundError:
            print(f"Файл не найден по данному пути {self.file_path}")
        except PermissionError:
            print(f"Нет доступа к файлу {self.file_path}")
        except UnicodeDecodeError:
            print(f"Неверная кодировка файла {self.file_path}")
        except json.JSONDecodeError:
            print(f"Некорректный JSON файл {self.file_path}")

        return []
