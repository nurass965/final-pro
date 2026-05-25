# Task Management System (To-Do App)

## Project Description

This is a Python console application for managing tasks and deadlines.  
The project was created for the **Introduction to Programming 2 (Python) Final Project**.

The system allows users to:

- Add tasks
- Edit tasks
- Delete tasks
- Set priorities and deadlines
- Mark tasks as completed
- Show tasks sorted by priority and deadline
- Show overdue tasks
- Show completion statistics
- Search tasks by keyword

## Technologies Used

- Python 3
- JSON file handling
- Object-Oriented Programming
- Modules and packages
- Unit testing with `unittest`

## Project Structure

```text
task_management_system/
│
├── main.py
├── README.md
│
├── data/
│   └── tasks.json
│
├── models/
│   ├── __init__.py
│   └── task.py
│
├── services/
│   ├── __init__.py
│   ├── file_service.py
│   └── task_manager.py
│
├── utils/
│   ├── __init__.py
│   ├── decorators.py
│   └── validators.py
│
└── tests/
    └── test_task_manager.py
```

## How to Run the Project

1. Open the project folder in PyCharm or VS Code.
2. Make sure Python 3 is installed.
3. Run this command:

```bash
python main.py
```

## How to Run Tests

```bash
python -m unittest discover tests
```

## Main Python Concepts Used

### Functions

The project uses functions with arguments and return values, for example:

- `add_task()`
- `edit_task()`
- `delete_task()`
- `get_statistics()`

### Control Flow

The console menu uses conditions and loops.

### Error Handling

The project uses exceptions for:

- invalid priority
- invalid status
- invalid deadline format
- task not found
- invalid JSON file

### Object-Oriented Programming

The project includes several classes:

1. `Task`
2. `WorkTask`
3. `PersonalTask`
4. `TaskManager`
5. `FileService`

OOP concepts:

- Encapsulation: private fields and properties in `Task`
- Inheritance: `WorkTask` and `PersonalTask` inherit from `Task`
- Polymorphism: `get_type()` works differently in child classes

### Collections and Data Structures

The project uses:

- List: for JSON input/output and sorted task results
- Dictionary: for fast task lookup by ID
- Tuple: in sorting key `(priority, deadline)`
- Set: for valid priorities and statuses

Dictionary is used because finding a task by ID is faster than searching through a list.

### File Handling

Tasks are stored in:

```text
data/tasks.json
```

The program reads from and writes to this JSON file.

### Algorithms and Efficiency

Tasks are stored in a dictionary:

```python
self.tasks = {}
```

This allows average **O(1)** lookup, edit, and delete by ID.

Sorting tasks uses:

```python
sorted(tasks, key=lambda task: (priority_order[task.priority], task.deadline))
```

Sorting complexity is **O(n log n)**.

### Advanced Python Features

The project uses:

- Generator: `upcoming_tasks_generator()`
- Decorator: `log_action`
- Lambda: used in statistics and sorting
- Regular expressions: date format validation

## Team Members

Write your team members here:

1. Student 1 — task model, OOP classes, file handling and JSON
2. Student 2 — task manager service and algorithms, testing and README

## Contribution Plan for GitHub

To show individual contributions, each student should make commits.

Example commit distribution:

### Student 1
- Add Task, WorkTask and PersonalTask classes
- Add validation for priority, status and deadline
- Add JSON file handling
- Add sample tasks
- Connect file saving/loading to main menu

### Student 2
- Add TaskManager class
- Add add/edit/delete/complete functions
- Add sorting, overdue tasks and statistics
- Add unit tests
- Add README documentation
- Test edge cases


## Example JSON Format

```json
[
    {
        "id": 1,
        "title": "Finish project report",
        "description": "Complete final project documentation",
        "priority": "high",
        "deadline": "2026-05-10",
        "status": "in_progress"
    }
]
```

## Defense Notes

During defense, explain:

- Why dictionary is used for storing tasks
- How JSON file loading and saving works
- How classes demonstrate OOP
- How sorting by priority and deadline works
- What tests check
- Where generator, decorator, lambda and regex are used
