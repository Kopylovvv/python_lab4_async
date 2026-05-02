import asyncio
from src.task import Task

from src.async_base import SimpleHandler, logger
from src.executor import AsyncExecutor


async def ainput(prompt: str) -> str:
    return await asyncio.to_thread(input, prompt)


async def main():
    print("--- Интерактивная платформа задач ---")
    print("Доступные команды: 'add', 'exit'")

    # Создаем исполнителя и регистрируем простой обработчик
    executor = AsyncExecutor(workers_count=2)
    executor.handler = SimpleHandler()

    async with executor:  # [cite: 1]
        while True:
            cmd = await ainput("\n> Введите команду: ")

            if cmd.strip().lower() == 'exit':
                logger.info("Выход из программы...")
                break

            if cmd.strip().lower() == 'add':
                tid = await ainput("ID задачи: ")
                info = await ainput("Описание: ")

                try:
                    task = Task(id=tid, payload={"info": info})
                    await executor.add_task(task)
                    print(f"Задача {tid} успешно добавлена.")
                except Exception as e:
                    print(f"Ошибка валидации: {e}")
            else:
                print("Неизвестная команда")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass