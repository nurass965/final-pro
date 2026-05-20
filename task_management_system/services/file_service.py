import json
from pathlib import Path


class FileService:
    """
    Handles reading and writing tasks to JSON files.
    """

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def load_tasks(self):
        if not self.file_path.exists():
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("JSON file must contain a list of tasks")

            return data

        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")

    def save_tasks(self, tasks):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)
