import asyncio
import logging
from typing import Protocol, runtime_checkable, Any
from src.task import Task

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("Processor")


@runtime_checkable
class TaskHandler(Protocol):
    async def handle(self, task: Task) -> Any:
        ...


class SimpleHandler:
    async def handle(self, task: Task) -> Any:
        await asyncio.sleep(1)  # Имитация работы
        return f"Выполнено для {task.id}"
