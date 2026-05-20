import re


def is_valid_date(date_text):
    """
    Regular expression example.
    Checks YYYY-MM-DD format.
    """
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return bool(re.match(pattern, date_text))


def ask_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Value cannot be empty.")
