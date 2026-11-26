import sys
from functools import wraps
from pathlib import Path

from logger.config import LogConfig, PipelineStep
from logger.exceptions import LogConfigurationError
from logger.tracking.tracker import FunctionTracker
from logger.validation.validation import validate_configuration

from .logger import log


def _get_steps(tracker) -> tuple[PipelineStep, ...]:
    return tuple(
        PipelineStep(**step) for step in tracker.get_steps(completed_only=True)
    )


def _display_success(action, target, result, tracker, display_mode):
    """Affiche le rapport de succès."""

    details = dict(result) if isinstance(result, dict) else {}

    log.success(
        LogConfig(
            project=Path.cwd().name,
            action=action,
            target=target,
            details=details,
            steps=_get_steps(tracker),
            display_mode=display_mode,
        )
    )


def _display_error(action, target, tracker, error, display_mode):
    """Affiche le rapport d'erreur."""

    log.error(
        LogConfig(
            project=Path.cwd().name,
            action=action,
            target=target,
            steps=_get_steps(tracker),
            display_mode=display_mode,
            error_message=str(error),
        )
    )


def log_pipeline(
    action=None,
    target=None,
    included_modules=None,
    excluded_modules=None,
    internal_exceptions=None,
    display_mode="simple",
):
    """Décorateur générique de suivi et de journalisation."""

    validate_configuration(
        action,
        excluded_modules,
        included_modules,
        internal_exceptions,
        target,
        display_mode,
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
                tracker.stop()
                _display_success(
                    action,
                    target,
                    result,
                    tracker,
                    display_mode,
                )

                return result

            except internal_exceptions as exc:
                tracker.stop()
                _display_error(
                    action,
                    target,
                    tracker,
                    exc,
                    display_mode,
                )

                raise

            finally:
                tracker.stop()

        return wrapper

    return decorator
