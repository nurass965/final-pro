from services.file_service import FileService
from services.task_manager import TaskManager
from utils.validators import ask_non_empty, is_valid_date


DATA_FILE = "data/tasks.json"


def print_task(task):
    print(
        f"ID: {task.id} | {task.title} | Priority: {task.priority} | "
        f"Deadline: {task.deadline} | Status: {task.status} | Type: {task.get_type()}"
    )


def print_menu():
    print("\n===== TASK MANAGEMENT SYSTEM =====")
    print("1. Show all tasks sorted by priority and deadline")
    print("2. Add task")
    print("3. Edit task")
    print("4. Delete task")
    print("5. Mark task as completed")
    print("6. Show overdue tasks")
    print("7. Show completion statistics")
    print("8. Search tasks")
    print("9. Show upcoming tasks using generator")
    print("0. Save and exit")


def choose_priority():
    while True:
        priority = input("Priority (low/medium/high): ").strip().lower()
        if priority in {"low", "medium", "high"}:
            return priority
        print("Invalid priority.")


def choose_status():
    while True:
        status = input("Status (pending/in_progress/completed): ").strip().lower()
        if status in {"pending", "in_progress", "completed"}:
            return status
        print("Invalid status.")


def choose_deadline():
    while True:
        deadline = input("Deadline (YYYY-MM-DD): ").strip()
        if is_valid_date(deadline):
            return deadline
        print("Invalid date format.")


def run_app():
    file_service = FileService(DATA_FILE)

    try:
        data = file_service.load_tasks()
        manager = TaskManager.from_list(data)
    except ValueError as error:
        print(f"Could not load data: {error}")
        manager = TaskManager()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                tasks = manager.get_sorted_tasks()
                if not tasks:
                    print("No tasks found.")
                for task in tasks:
                    print_task(task)

            elif choice == "2":
                title = ask_non_empty("Title: ")
                description = input("Description: ").strip()
                priority = choose_priority()
                deadline = choose_deadline()
                task_type = input("Task type (general/work/personal): ").strip().lower()

                extra = {}
                if task_type == "work":
                    extra["project_name"] = input("Project name: ").strip() or "General"
                elif task_type == "personal":
                    extra["category"] = input("Category: ").strip() or "Personal"
                else:
                    task_type = "general"

                task = manager.add_task(title, description, priority, deadline, task_type, extra)
                print("Task added:")
                print_task(task)

            elif choice == "3":
                task_id = int(input("Task ID: "))
                print("Leave field empty if you do not want to change it.")

                title = input("New title: ").strip() or None
                description = input("New description: ").strip() or None
                priority = input("New priority (low/medium/high): ").strip().lower() or None
                deadline = input("New deadline (YYYY-MM-DD): ").strip() or None
                status = input("New status (pending/in_progress/completed): ").strip().lower() or None

                task = manager.edit_task(task_id, title, description, priority, deadline, status)
                print("Task updated:")
                print_task(task)

            elif choice == "4":
                task_id = int(input("Task ID: "))
                manager.delete_task(task_id)
                print("Task deleted.")

            elif choice == "5":
                task_id = int(input("Task ID: "))
                task = manager.mark_completed(task_id)
                print("Task marked as completed:")
                print_task(task)

            elif choice == "6":
                overdue_tasks = manager.get_overdue_tasks()
                if not overdue_tasks:
                    print("No overdue tasks.")
                for task in overdue_tasks:
                    print_task(task)

            elif choice == "7":
                stats = manager.get_statistics()
                print("\nCompletion statistics:")
                for key, value in stats.items():
                    print(f"{key}: {value}")

            elif choice == "8":
                keyword = ask_non_empty("Search keyword: ")
                results = manager.search_tasks(keyword)
                if not results:
                    print("No matching tasks found.")
                for task in results:
                    print_task(task)

            elif choice == "9":
                print("Upcoming tasks:")
                found = False
                for task in manager.upcoming_tasks_generator():
                    found = True
                    print_task(task)
                if not found:
                    print("No upcoming tasks.")

            elif choice == "0":
                file_service.save_tasks(manager.to_list())
                print("Data saved. Goodbye!")
                break

            else:
                print("Invalid option.")

        except (ValueError, KeyError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    run_app()
