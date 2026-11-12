class LabToolkitError(Exception):
    """Exception de base de lab-toolkit."""


class ValidationError(LabToolkitError):
    """Exception contenant une ou plusieurs erreurs de validation."""

    def __init__(self, errors: list[str] | str):
        if isinstance(errors, str):
            errors = [errors]

        self.errors = errors

        message = "\n".join(f"- {error}" for error in errors)

        super().__init__(message)


class ConfigurationError(ValidationError):
    """Erreur liée à la configuration du projet."""


class BranchError(ValidationError):
    """Erreur liée à la branche Git."""


class GitError(LabToolkitError):
    """Erreur liée à l'exécution des commandes Git."""
