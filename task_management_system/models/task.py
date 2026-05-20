from dataclasses import dataclass
from datetime import datetime


VALID_PRIORITIES = {"low", "medium", "high"}
VALID_STATUSES = {"pending", "in_progress", "completed"}


@dataclass
class Task:
    """
    Base task class.
    Demonstrates encapsulation through private fields and properties.
    """
    _id: int
    _title: str
    _description: str
    _priority: str
    _deadline: str
    _status: str = "pending"

    def __post_init__(self):
        self.title = self._title
        self.description = self._description
        self.priority = self._priority
        self.deadline = self._deadline
        self.status = self._status

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not value.strip():
            raise ValueError("Task title cannot be empty")
        self._title = value.strip()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value.strip() if value else ""

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        if value not in VALID_PRIORITIES:
            raise ValueError("Priority must be: low, medium, or high")
        self._priority = value

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Deadline must be in YYYY-MM-DD format")
        self._deadline = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in VALID_STATUSES:
            raise ValueError("Status must be: pending, in_progress, or completed")
        self._status = value

    def mark_completed(self):
        self.status = "completed"

    def is_overdue(self, today=None):
        if self.status == "completed":
            return False
        today = today or datetime.today().date()
        deadline_date = datetime.strptime(self.deadline, "%Y-%m-%d").date()
        return deadline_date < today

    def get_type(self):
        # Polymorphism: child classes override this method
        return "general"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "deadline": self.deadline,
            "status": self.status,
            "type": self.get_type()
        }

    @staticmethod
    def from_dict(data):
        task_type = data.get("type", "general")

        if task_type == "work":
            return WorkTask(
                data["id"], data["title"], data.get("description", ""),
                data["priority"], data["deadline"], data.get("status", "pending"),
                data.get("project_name", "General")
            )

        if task_type == "personal":
            return PersonalTask(
                data["id"], data["title"], data.get("description", ""),
                data["priority"], data["deadline"], data.get("status", "pending"),
                data.get("category", "Personal")
            )

        return Task(
            data["id"], data["title"], data.get("description", ""),
            data["priority"], data["deadline"], data.get("status", "pending")
        )


class WorkTask(Task):
    """
    Inheritance example.
    WorkTask extends Task with project_name.
    """
    def __init__(self, task_id, title, description, priority, deadline, status="pending", project_name="General"):
        super().__init__(task_id, title, description, priority, deadline, status)
        self.project_name = project_name

    def get_type(self):
        return "work"

    def to_dict(self):
        data = super().to_dict()
        data["project_name"] = self.project_name
        return data


class PersonalTask(Task):
    """
    Inheritance example.
    PersonalTask extends Task with category.
    """
    def __init__(self, task_id, title, description, priority, deadline, status="pending", category="Personal"):
        super().__init__(task_id, title, description, priority, deadline, status)
        self.category = category

    def get_type(self):
        return "personal"

    def to_dict(self):
        data = super().to_dict()
        data["category"] = self.category
        return data
