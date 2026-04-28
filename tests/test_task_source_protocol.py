import pytest

from src.protocol import TaskSource
from src.task_sources.file_task_source import FileTaskSource
from src.task_sources.random_task_source import RandomTaskSource
from src.task_sources.api_task_source import APITaskSource
from src.task_sources.validation import validate_task_source


def test_task_source_protocol():
    file_source = FileTaskSource("tasks.json")
    random_source = RandomTaskSource(3)
    api_source = APITaskSource()

    assert isinstance(file_source, TaskSource)
    assert isinstance(random_source, TaskSource)
    assert isinstance(api_source, TaskSource)

    assert validate_task_source(file_source)
    assert validate_task_source(random_source)
    assert validate_task_source(api_source)


def test_task_source_protocol_negative():
    class NotASource:
        def get_something(self):
            return []

    not_source = NotASource()
    assert not isinstance(not_source, TaskSource)
    with pytest.raises(TypeError):
        validate_task_source(not_source)
