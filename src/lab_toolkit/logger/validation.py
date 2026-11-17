from lab_toolkit.logger.exceptions import LogConfigurationError


def validate_action(action):
    """Vérifie que le paramètre action est une chaîne non vide."""
    if action is None or not isinstance(action, str) or not action.strip():
        raise LogConfigurationError(
            "Le paramètre 'action' doit être une chaîne non vide."
        )


def validate_target(target):
    """Vérifie que le paramètre target est une chaîne non vide."""
    if target is None or not isinstance(target, str) or not target.strip():
        raise LogConfigurationError(
            "Le paramètre 'target' doit être une chaîne non vide."
        )


def validate_included_modules(included_modules):
    """Vérifie que les modules inclus sont des noms de modules valides."""
    if included_modules is None or not all(
        isinstance(module, str) and module.strip() for module in included_modules
    ):
        raise LogConfigurationError(
            "'included_modules' doit contenir des noms de modules."
        )


def validate_excluded_modules(excluded_modules):
    """Vérifie que les modules exclus sont des noms de modules valides."""
    if excluded_modules is None or not all(
        isinstance(module, str) and module.strip() for module in excluded_modules
    ):
        raise LogConfigurationError(
            "'excluded_modules' doit contenir des noms de modules."
        )


def validate_internal_exceptions(internal_exceptions):
    """Vérifie que les exceptions internes sont des classes d'exception."""
    if internal_exceptions is None:
        raise LogConfigurationError(
            "Le paramètre 'internal_exceptions' doit être renseigné "
            "avec une ou plusieurs classes d'exception."
        )

    if isinstance(internal_exceptions, type):
        internal_exceptions = (internal_exceptions,)

    if not isinstance(internal_exceptions, tuple) or not internal_exceptions:
        raise LogConfigurationError(
            "'internal_exceptions' doit contenir des classes d'exception."
        )

    if not all(
        isinstance(error, type) and issubclass(error, Exception)
        for error in internal_exceptions
    ):
        raise LogConfigurationError(
            "'internal_exceptions' doit contenir des classes d'exception."
        )


def validate_configuration(
    action,
    excluded_modules,
    included_modules,
    internal_exceptions,
    target,
):
    """Orchestre la validation de l'ensemble des paramètres de configuration."""
    validate_action(action)
    validate_target(target)
    validate_excluded_modules(excluded_modules)
    validate_included_modules(included_modules)
    validate_internal_exceptions(internal_exceptions)
