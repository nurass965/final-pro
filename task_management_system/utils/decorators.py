def log_action(func):
    """
    Decorator example.
    Prints action name when an important method is called.
    """
    def wrapper(*args, **kwargs):
        print(f"[LOG] Running: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
