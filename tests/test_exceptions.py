
from lab_toolkit.exceptions import (
    LabToolkitError,
    ValidationError,
    ConfigurationError,
    BranchError,
    GitError,
)


def test_validation_error_inherits_lab_toolkit_error():
    assert issubclass(ValidationError, LabToolkitError)


def test_configuration_error_inherits_validation_error():
    assert issubclass(ConfigurationError, ValidationError)


def test_branch_error_inherits_validation_error():
    assert issubclass(BranchError, ValidationError)


def test_git_error_inherits_lab_toolkit_error():
    assert issubclass(GitError, LabToolkitError)


def test_validation_error_stores_errors():
    errors = ["Erreur 1", "Erreur 2"]

    exception = ValidationError(errors)

    assert exception.errors == errors


def test_validation_error_formats_message():
    exception = ValidationError(["Erreur 1", "Erreur 2"])

    assert str(exception) == "- Erreur 1\n- Erreur 2"


def test_configuration_error_stores_errors():
    exception = ConfigurationError(["Configuration invalide"])

    assert exception.errors == ["Configuration invalide"]


def test_branch_error_stores_errors():
    exception = BranchError(["Branche invalide"])

    assert exception.errors == ["Branche invalide"]


def test_git_error_message():
    exception = GitError("Erreur Git")

    assert str(exception) == "Erreur Git"
