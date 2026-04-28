import pytest
from src.queue import TaskQueue, TaskIterator
from src.task import Task, Status, Priority


class TestTaskIterator:
    def setup_method(self):
        self.t1 = Task("1", {})
        self.t2 = Task("2", {})
        self.t1.description = "Task1"
        self.t2.description = "Task2"
        self.it = TaskIterator([self.t1, self.t2])

    def test_iterator_protocol(self):
        assert next(self.it) == self.t1
        assert next(self.it) == self.t2
        with pytest.raises(StopIteration):
            next(self.it)

    def test_empty_iterator(self):
        it = TaskIterator([])
        with pytest.raises(StopIteration):
            next(it)


class TestTaskQueue:
    def setup_method(self):
        self.t1 = Task("1", {})
        self.t2 = Task("2", {})
        self.t3 = Task("3", {})
        self.t1.description = "Task1"
        self.t2.description = "Task2"
        self.t3.description = "Task3"
        self.queue = TaskQueue([self.t1, self.t2, self.t3])

    def test_init_and_basic_props(self):
        assert len(self.queue) == 3
        assert self.queue.count == 3
        assert not self.queue.is_empty
        assert self.queue.tasks == (self.t1, self.t2, self.t3)
        assert repr(self.queue) == "TaskQueue(tasks=3)"

    def test_empty_queue(self):
        q = TaskQueue()
        assert len(q) == 0
        assert q.count == 0
        assert q.is_empty is True
        assert q.tasks == ()
        assert repr(q) == "TaskQueue(tasks=0)"

    def test_add_and_add_all(self):
        q = TaskQueue()
        t4 = Task("4", {})
        t5 = Task("5", {})
        t4.description = "Task4"
        t5.description = "Task5"
        q.add(self.t1)
        assert q.count == 1

    def test_add_invalid(self):
        q = TaskQueue()
        with pytest.raises(TypeError):
            q.add("not a task")
        with pytest.raises(TypeError):
            q.add(123)

    def test_remove_by_id(self):
        removed = self.queue.remove_by_id("2")
        assert removed == self.t2
        assert self.queue.count == 2
        assert self.queue.get_by_id("2") is None
        assert self.queue.get_by_id("1") == self.t1

        none = self.queue.remove_by_id("999")
        assert none is None

    def test_get_by_id(self):
        assert self.queue.get_by_id("1") == self.t1
        assert self.queue.get_by_id("2") == self.t2
        assert self.queue.get_by_id("3") == self.t3
        assert self.queue.get_by_id("999") is None

    def test_clear(self):
        self.queue.clear()
        assert self.queue.count == 0
        assert self.queue.is_empty is True
        assert len(self.queue) == 0

    def test_iteration(self):
        assert list(self.queue) == [self.t1, self.t2, self.t3]
        assert list(iter(self.queue)) == [self.t1, self.t2, self.t3]

        it1 = iter(self.queue)
        it2 = iter(self.queue)
        assert next(it1) == self.t1
        assert next(it2) == self.t1

    def test_stop_iteration(self):
        q = TaskQueue([self.t1])
        it = iter(q)
        assert next(it) == self.t1
        with pytest.raises(StopIteration):
            next(it)
        with pytest.raises(StopIteration):
            next(it)

    def test_getitem(self):
        assert self.queue[0] == self.t1
        assert self.queue[1] == self.t2
        assert self.queue[2] == self.t3
        assert self.queue[-1] == self.t3
        assert self.queue[-2] == self.t2
        with pytest.raises(IndexError):
            _ = self.queue[999]

    def test_getitem_slice(self):
        assert self.queue[0:2] == [self.t1, self.t2]
        assert self.queue[1:3] == [self.t2, self.t3]
        assert self.queue[:2] == [self.t1, self.t2]
        assert self.queue[1:] == [self.t2, self.t3]
        assert self.queue[:] == [self.t1, self.t2, self.t3]

    def test_setitem(self):
        t4 = Task("4", {})
        t4.description = "Task4"
        self.queue[1] = t4
        assert self.queue[1] == t4
        assert self.queue.count == 3

        with pytest.raises(TypeError):
            self.queue[0] = "not a task"

    def test_delitem(self):
        del self.queue[1]
        assert self.queue.count == 2
        assert self.queue[0] == self.t1
        assert self.queue[1] == self.t3

        del self.queue[0]
        assert self.queue.count == 1
        assert self.queue[0] == self.t3

    def test_tasks_setter(self):
        t4 = Task("4", {})
        t5 = Task("5", {})
        t4.description = "Task4"
        t5.description = "Task5"
        self.queue.tasks = [t4, t5]
        assert self.queue.count == 2
        assert self.queue[0] == t4
        assert self.queue[1] == t5

    def test_tasks_setter_invalid(self):
        with pytest.raises(TypeError):
            self.queue.tasks = "not a list"
        with pytest.raises(TypeError):
            self.queue.tasks = ["not a task", self.t1]

    def test_tasks_deleter(self):
        del self.queue.tasks
        assert self.queue.count == 0

    def test_filter_by_status(self):
        self.t1.status = Status.PENDING.value
        self.t2.status = Status.IN_PROGRESS.value
        self.t3.status = Status.COMPLETED.value

        assert list(self.queue.filter_by_status(Status.PENDING)) == [self.t1]
        assert list(self.queue.filter_by_status(Status.IN_PROGRESS)) == [self.t2]
        assert list(self.queue.filter_by_status(Status.COMPLETED)) == [self.t3]
        assert list(self.queue.filter_by_status(Status.FAILED)) == []

    def test_filter_by_priority(self):
        self.t1.priority = Priority.LOW.value
        self.t2.priority = Priority.MEDIUM.value
        self.t3.priority = Priority.HIGH.value

        assert list(self.queue.filter_by_priority(Priority.LOW)) == [self.t1]
        assert list(self.queue.filter_by_priority(Priority.MEDIUM)) == [self.t2]
        assert list(self.queue.filter_by_priority(Priority.HIGH)) == [self.t3]
    def test_filter_custom(self):
        assert list(self.queue.filter(lambda t: t.id in ["1", "3"])) == [self.t1, self.t3]
        assert list(self.queue.filter(lambda t: t.id == "999")) == []

    def test_iter_methods(self):
        self.t1.status = Status.PENDING.value
        self.t2.status = Status.IN_PROGRESS.value
        self.t3.status = Status.COMPLETED.value

        assert list(self.queue.iter_pending()) == [self.t1]
        assert list(self.queue.iter_in_progress()) == [self.t2]
        assert list(self.queue.iter_completed()) == [self.t3]
        assert list(self.queue.iter_active()) == [self.t1, self.t2]
        assert list(self.queue.iter_finished()) == [self.t3]

    def test_get_methods(self):
        self.t1.status = Status.PENDING.value
        self.t2.status = Status.IN_PROGRESS.value
        self.t3.status = Status.COMPLETED.value
        self.t1.priority = Priority.HIGH.value
        self.t2.priority = Priority.LOW.value

        assert self.queue.get_pending() == [self.t1]
        assert self.queue.get_in_progress() == [self.t2]
        assert self.queue.get_completed() == [self.t3]
        assert self.queue.get_active() == [self.t1, self.t2]
        assert self.queue.get_high_priority() == [self.t1]
        assert self.queue.get_low_priority() == [self.t2]


    def test_process_success(self):
        q = TaskQueue([self.t1])

        def processor(task):
            return "processed"

        results = list(q.process(processor))
        assert results[0].status_enum == Status.COMPLETED
        assert results[0].payload.get('result') == "processed"

    def test_process_failure(self):
        q = TaskQueue([self.t1])

        def processor(task):
            raise ValueError("Processing error")

        results = list(q.process(processor))
        assert results[0].status_enum == Status.FAILED
        assert 'error' in results[0].payload
        assert "Processing error" in results[0].payload['error']

    def test_process_skip_non_pending(self):
        self.t1.status = Status.COMPLETED.value
        q = TaskQueue([self.t1])

        def processor(task):
            return "done"

        results = list(q.process(processor))
        assert results[0].status_enum == Status.COMPLETED
        assert results[0].payload.get('result') is None

    def test_process_filtered(self):
        def processor(task):
            return "done"

        results = list(self.queue.process_filtered(processor, lambda t: t.id == "2"))
        assert results[0].status_enum == Status.PENDING
        assert results[1].status_enum == Status.COMPLETED
        assert results[2].status_enum == Status.PENDING