from typing import Iterator, Callable, Optional, Any, Union
from src.task import Task, Status, Priority


class TaskIterator:
    """
    класс итератора для независимых итераторов
    """

    def __init__(self, tasks: list[Task]):
        self._tasks = tasks
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._tasks):
            raise StopIteration
        task = self._tasks[self._index]
        self._index += 1
        return task


class TaskQueue:
    """
    очередь задач
    со всеми требованиями из тз:

    Функциональные требования:
        реализация протокола итерации;
        поддержка повторного обхода очереди;
        реализация ленивых фильтров (например, по статусу и приоритету);
        корректная работа с большими объёмами задач;
    Технические требования:
        использование генераторов для ленивых операций;
        отсутствие избыточного хранения данных в памяти;
        корректная обработка StopIteration;
    """

    def __init__(self, tasks: Optional[list[Task]] = None):
        """
        инициализация очереди

        args:
            tasks: начальный список задач
        """
        self._tasks: list[Task] = tasks if tasks is not None else []

    # доступ к задачам

    @property
    def tasks(self) -> tuple[Task, ...]:
        """возвращает кортеж задач, чтобы нельзя было изменить его"""
        return tuple(self._tasks)

    @tasks.setter
    def tasks(self, value: list[Task]) -> None:
        """устанавливает новый список задач"""
        if not isinstance(value, list):
            raise TypeError("tasks must be a list")
        if not all(isinstance(task, Task) for task in value):
            raise TypeError("all items must be Task instances")
        self._tasks = value

    @tasks.deleter
    def tasks(self) -> None:
        """удаляет все задачи"""
        self._tasks.clear()

    @property
    def count(self) -> int:
        """возвращает количество задач"""
        return len(self._tasks)

    @property
    def is_empty(self) -> bool:
        """проверяет, пуста ли очередь"""
        return len(self._tasks) == 0

    def add(self, task: Task) -> None:
        """добавляет задачу в очередь"""
        if not isinstance(task, Task):
            raise TypeError(f"Expected Task, got {type(task)}")
        self._tasks.append(task)

    def remove_by_id(self, task_id: str) -> Optional[Task]:
        """удаляет задачу по id и возвращает её"""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                return self._tasks.pop(i)
        return None

    def get_by_id(self, task_id: str) -> Optional[Task]:
        """возвращает задачу по id"""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def clear(self) -> None:
        """Очистить очередь"""
        self._tasks.clear()

    # протокол итерации

    def __iter__(self) -> TaskIterator:
        """возвращает отдельный и независимый итератор"""
        return TaskIterator(self._tasks)

    def __len__(self) -> int:
        return len(self._tasks)

    def __getitem__(self, index: Union[int, slice]) -> Union[Task, list[Task]]:
        """
        поддерживает доступ по индексу и срезам.
        """
        if isinstance(index, slice):
            return self._tasks[index]
        return self._tasks[index]

    def __setitem__(self, index: int, task: Task) -> None:
        """устанавливает задачу по индексу"""
        if not isinstance(task, Task):
            raise TypeError(f"Expected Task, got {type(task)}")
        self._tasks[index] = task

    def __delitem__(self, index: int) -> None:
        """удаляет задачу по индексу"""
        del self._tasks[index]

    # генераторы/фильтры

    def filter_by_status(self, status: Status) -> Iterator[Task]:
        """фильтрация задач по статусу"""
        for task in self._tasks:
            if task.status_enum == status:
                yield task

    def filter_by_priority(self, priority: Priority) -> Iterator[Task]:
        """
        фильтрация задач по приоритету.
        """
        for task in self._tasks:
            if task.priority_enum.value == priority.value:
                yield task

    def filter(self, predicate: Callable[[Task], bool]) -> Iterator[Task]:
        """фильтрация по пользовательскому предикату"""
        for task in self._tasks:
            if predicate(task):
                yield task

    # получение списков задач

    def get_pending(self) -> list[Task]:
        """возвращает список ожидающих задач"""
        return list(self.filter_by_status(Status.PENDING))

    def get_in_progress(self) -> list[Task]:
        """возвращает список выполняемых задач"""
        return list(self.filter_by_status(Status.IN_PROGRESS))

    def get_completed(self) -> list[Task]:
        """возвращает список выполненных задач"""
        return list(self.filter_by_status(Status.COMPLETED))

    def get_failed(self) -> list[Task]:
        """возвращает список проваленных задач"""
        return list(self.filter_by_status(Status.FAILED))

    def get_cancelled(self) -> list[Task]:
        """возвращает список отменённых задач"""
        return list(self.filter_by_status(Status.CANCELLED))

    def get_active(self) -> list[Task]:
        """возвращает список активных задач (pending или in_progress)"""
        return list(self.filter(lambda t: t.is_active))

    def get_finished(self) -> list[Task]:
        """возвращает список завершённых задач (completed, cancelled, failed)"""
        return list(self.filter(lambda t: t.is_finished))

    def get_high_priority(self) -> list[Task]:
        """возвращает список высокоприоритетных задач (high)"""
        return list(self.filter_by_priority(Priority.HIGH))

    def get_low_priority(self) -> list[Task]:
        """возвращает список низкоприоритетных задач (low)"""
        return list(self.filter_by_priority(Priority.LOW))

    # ========== ленивые итераторы ==========

    def iter_pending(self) -> Iterator[Task]:
        """итерация по ожидающим задачам"""
        return self.filter_by_status(Status.PENDING)

    def iter_in_progress(self) -> Iterator[Task]:
        """итерация по выполняемым задачам"""
        return self.filter_by_status(Status.IN_PROGRESS)

    def iter_completed(self) -> Iterator[Task]:
        """итерация по выполненным задачам"""
        return self.filter_by_status(Status.COMPLETED)

    def iter_failed(self) -> Iterator[Task]:
        """итерация по проваленным задачам"""
        return self.filter_by_status(Status.FAILED)

    def iter_cancelled(self) -> Iterator[Task]:
        """итерация по отменённым задачам"""
        return self.filter_by_status(Status.CANCELLED)

    def iter_active(self) -> Iterator[Task]:
        """итерация по активным задачам"""
        return self.filter(lambda t: t.is_active)

    def iter_finished(self) -> Iterator[Task]:
        """итерация по завершённым задачам"""
        return self.filter(lambda t: t.is_finished)

    # обработка

    def process(self, processor: Callable[[Task], Any]) -> Iterator[Task]:
        """
        обрабатывает задачи с ленивым выполнением
        задача переходит в статус in_progress, затем в completed или failed
        если итерация прерывается, задача может остаться в in_progress
        """
        for task in self._tasks:
            if task.status_enum != Status.PENDING:
                yield task
                continue

            task.start()
            try:
                result = processor(task)
                task.payload['result'] = result
                task.complete()
            except Exception as e:
                task.payload['error'] = str(e)
                task.fail()
            yield task

    def process_filtered(self, processor: Callable[[Task], Any],
                         filter_predicate: Callable[[Task], bool]) -> Iterator[Task]:
        """
        обрабатывает только задачи, прошедшие фильтр
        остальные задачи возвращаются без изменений
        """
        for task in self._tasks:
            if filter_predicate(task) and task.status_enum == Status.PENDING:
                task.start()
                try:
                    result = processor(task)
                    task.payload['result'] = result
                    task.complete()
                except Exception as e:
                    task.payload['error'] = str(e)
                    task.fail()
            yield task

    def __repr__(self) -> str:
        return f"TaskQueue(tasks={len(self._tasks)})"
