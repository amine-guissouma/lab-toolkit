import sys
from functools import wraps
from pathlib import Path

from lab_toolkit.logger import LogConfig, log
from lab_toolkit.logger.config import PipelineStep
from lab_toolkit.logger.exceptions import LogConfigurationError
from lab_toolkit.logger.tracker import FunctionTracker
from lab_toolkit.logger.validation import validate_configuration


def _get_steps(tracker) -> tuple[PipelineStep, ...]:
    return tuple(
        PipelineStep(**step) for step in tracker.get_steps(completed_only=True)
    )


def _display_success(action, target, result, tracker):
    """Affiche le rapport de succès."""
    details = dict(result) if isinstance(result, dict) else {}

    log.success(
        LogConfig(
            project=Path.cwd().name,
            action=action,
            target=target,
            details=details,
            steps=_get_steps(tracker),
        )
    )


def _display_error(action, target, tracker):
    """Affiche le rapport d'erreur métier."""
    log.error(
        LogConfig(
            project=Path.cwd().name,
            action=action,
            target=target,
            steps=_get_steps(tracker),
        )
    )


def log_pipeline(
    action=None,
    target=None,
    included_modules=None,
    excluded_modules=None,
    internal_exceptions=None,
):
    """Décorateur générique de suivi et de journalisation d'un pipeline."""

    validate_configuration(
        action,
        excluded_modules,
        included_modules,
        internal_exceptions,
        target,
    )

    def decorator(func):

        if not callable(func):
            raise LogConfigurationError("'log_pipeline' doit décorer une fonction.")

        @wraps(func)
        def wrapper(*args, **kwargs):

            tracker = FunctionTracker(
                root_frame=sys._getframe(),
                included_modules=included_modules,
                excluded_modules=excluded_modules,
            )

            try:
                tracker.start()

                result = func(*args, **kwargs)
                _display_success(action, target, result, tracker)

                return result

            except internal_exceptions:
                _display_error(action, target, tracker)
                raise

            finally:
                tracker.stop()

        return wrapper

    return decorator
