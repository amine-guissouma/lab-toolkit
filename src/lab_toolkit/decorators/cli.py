from functools import wraps

from lab_toolkit.cli.exception import CliConfigurationError


def validate_internal_exceptions(internal_exceptions):
    """Vérifie que les exceptions internes sont des classes d'exception."""
    if internal_exceptions is None:
        raise CliConfigurationError(
            "Le paramètre 'internal_exceptions' doit être renseigné "
            "avec une ou plusieurs classes d'exception."
        )

    if isinstance(internal_exceptions, type):
        internal_exceptions = (internal_exceptions,)

    if not isinstance(internal_exceptions, tuple) or not internal_exceptions:
        raise CliConfigurationError(
            "'internal_exceptions' doit contenir des classes d'exception."
        )

    if not all(
        isinstance(error, type) and issubclass(error, Exception)
        for error in internal_exceptions
    ):
        raise CliConfigurationError(
            "'internal_exceptions' doit contenir des classes d'exception."
        )


def handle_errors(internal_exceptions=None):
    """
    Gère le code de sortie de la commande CLI.

    Retourne :
        0 : commande exécutée sans exception.
        1 : une exception gérée est survenue.
    """
    validate_internal_exceptions(internal_exceptions)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except internal_exceptions:
                return 1
            return 0

        return wrapper

    return decorator
