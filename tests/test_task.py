import time
import pytest
from src.task import Task, Priority, Status
from src.exceptions import TaskValidationError, InvalidTaskStateError


def test_task_creation_minimal():
    task = Task(id="1", payload="data")
    assert task.id == "1"
    assert task.payload == "data"
    assert task.description == "Задача 1"
    assert task.priority == "обычный"
    assert task.status == "не начата"
    assert task.created_at > 0


def test_task_creation_full():
    task = Task(
        id="2",
        payload={"order": 123,
                 "description": "Тестовая задача",
                 "priority": "высокий"}
    )
    assert task.id == "2"
    assert task.payload == {"order": 123,
                            "description": "Тестовая задача",
                            "priority": "высокий"}
    assert task.description == "Тестовая задача"
    assert task.priority == "высокий"
    assert task.status == "не начата"


def test_task_creation_with_enum():
    task = Task(id="3", payload={"priority": Priority.HIGH}, )
    assert task.priority == "высокий"
    assert task.priority_enum == Priority.HIGH


def test_task_creation_invalid_id():
    with pytest.raises(TaskValidationError):
        Task(id="", payload="data")
    with pytest.raises(TaskValidationError):
        Task(id=None, payload="data")  # type: ignore


def test_task_creation_invalid_priority():
    with pytest.raises(TaskValidationError):
        Task(id="4", payload={"priority": "неверный"})


def test_task_properties():
    task = Task(id="5", payload={"description": "Тест"})

    assert task.age >= 0
    assert task.can_edit is True
    assert task.can_start is True
    assert task.is_active is True
    assert task.is_finished is False

    time.sleep(0.1)
    assert task.age > 0


def test_task_edit_before_start():
    task = Task(id="6", payload={"description": "Старое", "priority": "низкий"})

    task.edit(description="Новое", priority="высокий")

    assert task.description == "Новое"
    assert task.priority == "высокий"


def test_task_edit_partial():
    task = Task(id="7", payload={"description": "Описание", "priority": "низкий"})

    task.edit(description="Новое описание")
    assert task.description == "Новое описание"
    assert task.priority == "низкий"

    task.edit(priority="высокий")
    assert task.priority == "высокий"


def test_task_edit_after_start():
    task = Task(id="8", payload={"description": "Описание"})
    task.start()

    with pytest.raises(InvalidTaskStateError):
        task.edit(description="Новое")


def test_task_status_lifecycle():
    task = Task(id="9", payload={"description": "Описание"})

    assert task.status == "не начата"
    assert task.status_enum == Status.PENDING

    task.start()
    assert task.status == "в работе"
    assert task.status_enum == Status.IN_PROGRESS

    task.complete()
    assert task.status == "завершена"
    assert task.status_enum == Status.COMPLETED


def test_task_cancel():
    task = Task(id="10", payload={"description": "Описание"})
    task.cancel()
    assert task.status == "отменена"
    assert task.status_enum == Status.CANCELLED


def test_task_fail():
    task = Task(id="11", payload={"description": "Описание"})
    task.start()
    task.fail()
    assert task.status == "провалена"
    assert task.status_enum == Status.FAILED


def test_task_invalid_transitions():
    task = Task(id="12", payload={"description": "Описание"})

    with pytest.raises(InvalidTaskStateError):
        task.complete()

    task.start()

    with pytest.raises(InvalidTaskStateError):
        task.start()

    task.complete()

    with pytest.raises(InvalidTaskStateError):
        task.start()

    with pytest.raises(InvalidTaskStateError):
        task.cancel()
