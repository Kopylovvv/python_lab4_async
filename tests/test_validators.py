import pytest
from src.validators import validate_string, validate_priority, validate_status
from src.task import Priority, Status


def test_validate_string_valid():
    assert validate_string("test") == "test"
    assert validate_string("  hello  ") == "hello"
    assert validate_string("123") == "123"


def test_validate_string_invalid_type():
    with pytest.raises(TypeError):
        validate_string(123)
    with pytest.raises(TypeError):
        validate_string(None)
    with pytest.raises(TypeError):
        validate_string([])


def test_validate_string_empty():
    with pytest.raises(ValueError):
        validate_string("")
    with pytest.raises(ValueError):
        validate_string("   ")
    with pytest.raises(ValueError):
        validate_string("\n\t")


def test_validate_priority_string():
    assert validate_priority("низкий") == "низкий"
    assert validate_priority("обычный") == "обычный"
    assert validate_priority("высокий") == "высокий"


def test_validate_priority_enum():
    assert validate_priority(Priority.LOW) == "низкий"
    assert validate_priority(Priority.MEDIUM) == "обычный"
    assert validate_priority(Priority.HIGH) == "высокий"


def test_validate_priority_invalid():
    with pytest.raises(ValueError):
        validate_priority("сверхсрочный")
    with pytest.raises(ValueError):
        validate_priority("")
    with pytest.raises(TypeError):
        validate_priority(123)


def test_validate_status_string():
    assert validate_status("не начата") == "не начата"
    assert validate_status("в работе") == "в работе"
    assert validate_status("завершена") == "завершена"
    assert validate_status("отменена") == "отменена"
    assert validate_status("провалена") == "провалена"


def test_validate_status_enum():
    assert validate_status(Status.PENDING) == "не начата"
    assert validate_status(Status.IN_PROGRESS) == "в работе"
    assert validate_status(Status.COMPLETED) == "завершена"
    assert validate_status(Status.CANCELLED) == "отменена"
    assert validate_status(Status.FAILED) == "провалена"


def test_validate_status_invalid():
    with pytest.raises(ValueError):
        validate_status("неизвестно")
    with pytest.raises(ValueError):
        validate_status("")
    with pytest.raises(TypeError):
        validate_status(123)