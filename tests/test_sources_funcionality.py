from src.task_sources.file_task_source import FileTaskSource
from src.task_sources.random_task_source import RandomTaskSource
from src.task_sources.api_task_source import APITaskSource
from src.task import Task


def test_sources_functionality():
    file_source = FileTaskSource("tests/tasks.json")
    random_source = RandomTaskSource(2)
    api_source = APITaskSource()

    file_tasks = file_source.get_tasks()
    assert len(file_tasks) == 3
    assert all(isinstance(t, Task) for t in file_tasks)
    assert all(isinstance(t.id, str) for t in file_tasks)

    random_tasks = random_source.get_tasks()
    assert len(random_tasks) == 2
    assert all(isinstance(t, Task) for t in random_tasks)

    api_tasks = api_source.get_tasks()
    assert len(api_tasks) == 3
    assert all(isinstance(t, Task) for t in api_tasks)
