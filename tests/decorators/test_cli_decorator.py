import pytest

from cli.core.decorators import handle_errors
from cli.core.exception import CliConfigurationError
from lab_toolkit.exceptions import (
    ConfigurationError,
    GitError,
    LabToolkitError,
)


def test_handle_errors_success():
    # prepare

    executed = []

    @handle_errors((LabToolkitError,))
    def command():
        executed.append(True)

    # execute
    result = command()

    # test
    assert result == 0
    assert executed == [True]


def test_handle_errors_configuration_error():
    # prepare
    @handle_errors((LabToolkitError,))
    def command():
        raise ConfigurationError(["Configuration invalide"])

    # execute
    result = command()

    # test
    assert result == 1


def test_handle_errors_git_error():
    # prepare
    @handle_errors((LabToolkitError,))
    def command():
        raise GitError("Erreur Git")

    # execute
    result = command()

    # test
    assert result == 1


def test_handle_errors_unexpected_exception():
    # prepare
    @handle_errors((LabToolkitError,))
    def command():
        raise ValueError("Erreur inattendue")

    # execute / test
    with pytest.raises(ValueError, match="Erreur inattendue"):
        command()


@pytest.mark.parametrize(
    "internal_exceptions",
    [
        None,
        (),
        "LabToolkitError",
        (str,),
    ],
)
def test_handle_errors_requires_internal_exceptions(internal_exceptions):
    # execute / test
    with pytest.raises(CliConfigurationError):
        handle_errors(internal_exceptions)
