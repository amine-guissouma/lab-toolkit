from functools import wraps

from lab_toolkit.cli.application.config import EXCLUDED_MODULES, INCLUDED_MODULES
from lab_toolkit.cli.core.decorators.cli import handle_errors
from lab_toolkit.exceptions import LabToolkitError
from lab_toolkit.logger.core.pipeline import log_pipeline


def cli_command(
    *,
    action: str,
    target: str,
    included_modules=INCLUDED_MODULES,
    excluded_modules=EXCLUDED_MODULES,
    display_mode: str = "pipeline",
):
    """Décorateur central des commandes CLI."""

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            selected_display_mode = display_mode

            command_args = args[0] if args else kwargs.get("args")

            if command_args is not None:
                selected_display_mode = getattr(
                    command_args,
                    "display_mode",
                    display_mode,
                )

            decorated_func = log_pipeline(
                action=action,
                target=target,
                included_modules=included_modules,
                excluded_modules=excluded_modules,
                internal_exceptions=(LabToolkitError,),
                display_mode=selected_display_mode,
            )(func)

            return decorated_func(*args, **kwargs)

        return handle_errors((LabToolkitError,))(wrapper)

    return decorator
