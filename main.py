from src.queue import TaskQueue
from src.task import Task, Status, Priority
from src.task_sources.random_task_source import RandomTaskSource


def main():
    # 1. Создание задач через RandomTaskSource
    print("1. Генерация задач через RandomTaskSource:")
    source = RandomTaskSource(count=3)
    tasks = source.get_tasks()
    for task in tasks:
        print(f"   {task.id}: {task.description} (приоритет: {task.priority})")

    # 2. Создание очереди и добавление задач
    print("\n2. Создание очереди и добавление задач:")
    queue = TaskQueue()
    for task in tasks:
        queue.add(task)
    print(f"   В очереди {queue.count} задач")

    # 3. Итерация по очереди (первый обход)
    print("\n3. Первый обход очереди:")
    for task in queue:
        print(f"   {task.id}")

    # 4. Повторный обход очереди
    print("\n4. Повторный обход очереди (поддержка повторной итерации):")
    for task in queue:
        print(f"   {task.id}")

    # 5. Фильтрация по статусу (ленивый генератор)
    print("\n5. Фильтрация по статусу PENDING:")
    pending_tasks = list(queue.filter_by_status(Status.PENDING))
    print(f"   Найдено {len(pending_tasks)} задач в статусе 'не начата'")
    for task in pending_tasks:
        print(f"   {task.id}")

    # 6. Изменение статуса задачи
    print("\n6. Изменение статуса задачи:")
    first_task = queue[0]
    print(f"   До: {first_task.id} - {first_task.status}")
    first_task.start()
    first_task.complete()
    print(f"   После: {first_task.id} - {first_task.status}")

    # 7. Фильтрация по завершённым задачам
    print("\n7. Фильтрация по статусу COMPLETED:")
    completed_tasks = list(queue.filter_by_status(Status.COMPLETED))
    print(f"   Найдено {len(completed_tasks)} завершённых задач")

    # 8. Фильтрация по приоритету
    print("\n8. Фильтрация по приоритету HIGH:")
    high_priority = list(queue.filter_by_priority(Priority.HIGH))
    print(f"   Найдено {len(high_priority)} задач с высоким приоритетом")

    # 9. Пользовательский фильтр
    print("\n9. Пользовательский фильтр (задачи с ID содержащим '0'):")
    custom_filter = list(queue.filter(lambda t: '0' in t.id))
    print(f"   Найдено {len(custom_filter)} задач")

    # 11. Потоковая обработка задач
    print("\n11. Потоковая обработка задач (process):")

    def simple_processor(task):
        return f"обработано_{task.id}"

    for task in queue.process(simple_processor):
        if task.status_enum == Status.COMPLETED:
            print(f"   {task.id} -> завершена, результат: {task.payload.get('result')}")
        elif task.status_enum == Status.FAILED:
            print(f"   {task.id} -> ошибка: {task.payload.get('error')}")

    # 12. Получение задачи по ID
    print("\n12. Получение задачи по ID:")
    task_id = tasks[0].id
    found_task = queue.get_by_id(task_id)
    print(f"   Задача {task_id} найдена, статус: {found_task.status if found_task else 'не найдена'}")

    # 13. Удаление задачи по ID
    print("\n13. Удаление задачи по ID:")
    removed = queue.remove_by_id(task_id)
    print(f"   Удалена задача: {removed.id if removed else 'не найдена'}")
    print(f"   В очереди осталось {queue.count} задач")

    # 14. Доступ по индексу
    print("\n14. Доступ по индексу:")
    if queue.count > 0:
        print(f"   Первая задача: {queue[0].id}")
        print(f"   Последняя задача: {queue[-1].id}")

    # 15. Длина очереди
    print("\n15. Длина очереди (__len__):")
    print(f"   len(queue) = {len(queue)}")

    # 16. Очистка очереди
    print("\n16. Очистка очереди:")
    queue.clear()
    print(f"   После очистки: {queue.count} задач")

    # 17. Проверка на пустоту
    print("\n17. Проверка на пустоту:")
    print(f"   queue.is_empty = {queue.is_empty}")

    # 18. Демонстрация StopIteration
    print("\n18. Демонстрация StopIteration:")
    queue.add(Task(id="test_001", payload={}))
    queue[0].description = "Тестовая задача"
    iterator = iter(queue)
    print(f"   {next(iterator).id}")
    try:
        next(iterator)
    except StopIteration:
        print("   StopIteration перехвачен - итерация завершена")

    # 19. Повторное использование итератора
    print("\n19. Повторный обход после StopIteration:")
    for task in queue:
        print(f"   {task.id}")


if __name__ == "__main__":
    main()