from datetime import datetime
from models.task import Task, WorkTask, PersonalTask
from utils.decorators import log_action


class TaskManager:
    """
    Service class that manages task operations.
    Uses dictionary for O(1) average lookup by task id.
    """

    PRIORITY_ORDER = {
        "high": 1,
        "medium": 2,
        "low": 3
    }

    def __init__(self, tasks=None):
        # Dictionary is used instead of list for faster search/edit/delete by id
        self.tasks = {}
        if tasks:
            for task in tasks:
                self.tasks[task.id] = task

    def generate_id(self):
        if not self.tasks:
            return 1
        return max(self.tasks.keys()) + 1

    @log_action
    def add_task(self, title, description, priority, deadline, task_type="general", extra=None):
        task_id = self.generate_id()
        extra = extra or {}

        if task_type == "work":
            task = WorkTask(task_id, title, description, priority, deadline, "pending", extra.get("project_name", "General"))
        elif task_type == "personal":
            task = PersonalTask(task_id, title, description, priority, deadline, "pending", extra.get("category", "Personal"))
        else:
            task = Task(task_id, title, description, priority, deadline)

        self.tasks[task_id] = task
        return task

    @log_action
    def edit_task(self, task_id, title=None, description=None, priority=None, deadline=None, status=None):
        task = self.get_task(task_id)

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority
        if deadline is not None:
            task.deadline = deadline
        if status is not None:
            task.status = status

        return task

    @log_action
    def delete_task(self, task_id):
        if task_id not in self.tasks:
            raise KeyError("Task was not found")
        return self.tasks.pop(task_id)

    def get_task(self, task_id):
        if task_id not in self.tasks:
            raise KeyError("Task was not found")
        return self.tasks[task_id]

    @log_action
    def mark_completed(self, task_id):
        task = self.get_task(task_id)
        task.mark_completed()
        return task

    def get_sorted_tasks(self):
        # Sorting by priority first, then by deadline
        return sorted(
            self.tasks.values(),
            key=lambda task: (self.PRIORITY_ORDER[task.priority], task.deadline)
        )

    def get_overdue_tasks(self, today=None):
        return [task for task in self.tasks.values() if task.is_overdue(today)]

    def get_statistics(self):
        total = len(self.tasks)

        if total == 0:
            return {
                "total": 0,
                "completed": 0,
                "pending": 0,
                "in_progress": 0,
                "completion_rate": 0
            }

        completed = len(list(filter(lambda task: task.status == "completed", self.tasks.values())))
        pending = len(list(filter(lambda task: task.status == "pending", self.tasks.values())))
        in_progress = len(list(filter(lambda task: task.status == "in_progress", self.tasks.values())))

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "in_progress": in_progress,
            "completion_rate": round((completed / total) * 100, 2)
        }

    def search_tasks(self, keyword):
        keyword = keyword.lower()
        return [
            task for task in self.tasks.values()
            if keyword in task.title.lower() or keyword in task.description.lower()
        ]

    def upcoming_tasks_generator(self):
        """
        Generator example.
        It yields tasks one by one instead of creating a full list in memory.
        """
        today = datetime.today().date()
        for task in self.get_sorted_tasks():
            deadline_date = datetime.strptime(task.deadline, "%Y-%m-%d").date()
            if deadline_date >= today and task.status != "completed":
                yield task

    def to_list(self):
        return [task.to_dict() for task in self.tasks.values()]

    @classmethod
    def from_list(cls, data):
        tasks = [Task.from_dict(item) for item in data]
        return cls(tasks)
