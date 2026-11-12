from functools import wraps

from lab_toolkit.exceptions import LabToolkitError


def handle_errors(success_message: str):
    """Gère les exceptions et les messages des commandes CLI."""

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)

            except LabToolkitError as error:
                print(f"ERREUR : {error}")
                return 1

            print(success_message)
            return 0

        return wrapper

    return decorator
