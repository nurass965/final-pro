import unittest
from datetime import date

from models.task import Task
from services.task_manager import TaskManager


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.manager = TaskManager()
        self.manager.add_task("A", "Test A", "low", "2026-05-30")
        self.manager.add_task("B", "Test B", "high", "2026-05-20")
        self.manager.add_task("C", "Test C", "medium", "2026-05-25")

    def test_add_task(self):
        task = self.manager.add_task("New task", "Description", "high", "2026-06-01")
        self.assertEqual(task.title, "New task")
        self.assertEqual(len(self.manager.tasks), 4)

    def test_sorting_by_priority_and_deadline(self):
        sorted_tasks = self.manager.get_sorted_tasks()
        self.assertEqual(sorted_tasks[0].priority, "high")
        self.assertEqual(sorted_tasks[-1].priority, "low")

    def test_mark_completed(self):
        self.manager.mark_completed(1)
        self.assertEqual(self.manager.get_task(1).status, "completed")

    def test_delete_task(self):
        self.manager.delete_task(1)
        self.assertNotIn(1, self.manager.tasks)

    def test_overdue_task(self):
        task = Task(10, "Old task", "Past deadline", "high", "2026-01-01")
        self.assertTrue(task.is_overdue(date(2026, 5, 21)))

    def test_invalid_priority(self):
        with self.assertRaises(ValueError):
            self.manager.add_task("Bad task", "Invalid", "urgent", "2026-05-30")

    def test_statistics(self):
        self.manager.mark_completed(1)
        stats = self.manager.get_statistics()
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["completed"], 1)


if __name__ == "__main__":
    unittest.main()
