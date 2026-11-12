
import pytest

from lab_toolkit.decorators.cli import handle_errors
from lab_toolkit.exceptions import (
    ConfigurationError,
    GitError,
)


def test_handle_errors_success(capsys):
    @handle_errors("Opération réussie.")
    def command():
        pass

    result = command()

    captured = capsys.readouterr()

    assert result == 0
    assert captured.out == "Opération réussie.\n"


def test_handle_errors_configuration_error(capsys):
    @handle_errors("Opération réussie.")
    def command():
        raise ConfigurationError(["Configuration invalide"])

    result = command()

    captured = capsys.readouterr()

    assert result == 1
    assert captured.out == (
        "ERREUR : - Configuration invalide\n"
    )


def test_handle_errors_git_error(capsys):
    @handle_errors("Opération réussie.")
    def command():
        raise GitError("Erreur Git")

    result = command()

    captured = capsys.readouterr()

    assert result == 1
    assert captured.out == "ERREUR : Erreur Git\n"


def test_handle_errors_unexpected_exception():
    @handle_errors("Opération réussie.")
    def command():
        raise ValueError("Erreur inattendue")

    with pytest.raises(ValueError, match="Erreur inattendue"):
        command()
