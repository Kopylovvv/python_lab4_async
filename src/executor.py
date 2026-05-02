import asyncio
from src.async_base import logger, TaskHandler
from src.task import Task


class AsyncExecutor:
    def __init__(self, workers_count: int = 3):
        self.queue = asyncio.Queue()
        self.workers_count = workers_count
        self.handler: TaskHandler = None
        self._workers = []

    async def add_task(self, task: Task):
        await self.queue.put(task)

    async def _worker(self, name: str):
        while True:
            task = await self.queue.get()
            try:
                if task.can_start:
                    task.start()
                    logger.info(f"[{name}] Взял задачу: {task.id}")
                    res = await self.handler.handle(task)
                    task.payload['result'] = res
                    task.complete()
                    logger.info(f"[{name}] Завершил: {task.id}")
            except Exception as e:
                task.fail()
                logger.error(f"[{name}] Ошибка {task.id}: {e}")
            finally:
                self.queue.task_done()

    async def __aenter__(self):
        self._workers = [asyncio.create_task(self._worker(f"W-{i}")) for i in range(self.workers_count)]
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        for w in self._workers:
            w.cancel()
