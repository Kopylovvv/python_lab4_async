from src.task_sources.file_task_source import FileTaskSource
from src.task_sources.validation import validate_task_source


def test_task_source_validation():
    file_source = FileTaskSource("tasks.json")
    assert validate_task_source(file_source)

def test_task_source_validation_negative():
    class BadSource:
        def get_tasks(self):
            return "not a list"

    bad_source = BadSource()

    try:
        validate_task_source(bad_source)
        assert False, "Должна быть ошибка TypeError"
    except TypeError as e:
        assert "должен возвращать список" in str(e)