from typing import Protocol, runtime_checkable
from src.task import Task


@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> list[Task]:
        ...
