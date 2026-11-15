from types import SimpleNamespace

import pytest

from lab_toolkit.cli.commands import deployment
from lab_toolkit.exceptions import BranchError, ConfigurationError


def test_validate_calls_pipeline(monkeypatch, capsys):
    called = []

    monkeypatch.setattr(
        deployment,
        "validate_pipeline",
        lambda: called.append(True),
    )

    result = deployment.validate(SimpleNamespace())

    output = capsys.readouterr().out

    assert result == 0
    assert called == [True]
    assert output == "Configuration de déploiement valide.\n"


def test_show_config_calls_pipeline(monkeypatch, capsys):
    called = []

    monkeypatch.setattr(
        deployment,
        "show_config_pipeline",
        lambda: called.append(True),
    )

    result = deployment.show_config(SimpleNamespace())

    output = capsys.readouterr().out

    assert result == 0
    assert called == [True]
    assert output == "Aucune modification effectuée.\n"


def test_apply_config_calls_pipeline(monkeypatch, capsys):
    called = []

    monkeypatch.setattr(
        deployment,
        "apply_config_pipeline",
        lambda: called.append(True),
    )

    result = deployment.apply_config(SimpleNamespace())

    output = capsys.readouterr().out

    assert result == 0
    assert called == [True]
    assert output == "Configuration de déploiement mise à jour.\n"


@pytest.mark.parametrize(
    ("command", "pipeline_name", "exception"),
    [
        ("show_config", "show_config_pipeline", BranchError),
        ("apply_config", "apply_config_pipeline", ConfigurationError),
    ],
)
def test_commands_handle_pipeline_errors(
    monkeypatch,
    capsys,
    command,
    pipeline_name,
    exception,
):
    def raise_error():
        raise exception(["Erreur de test"])

    monkeypatch.setattr(deployment, pipeline_name, raise_error)

    result = getattr(deployment, command)(SimpleNamespace())

    output = capsys.readouterr().out

    assert result == 1
    assert "ERREUR : - Erreur de test" in output


def test_init_calls_pipeline(monkeypatch, capsys):
    """Vérifie que la commande init appelle son pipeline."""

    called = []

    monkeypatch.setattr(
        deployment,
        "init_config_pipeline",
        lambda: called.append(True),
    )

    result = deployment.init(SimpleNamespace())

    output = capsys.readouterr().out

    assert result == 0
    assert called == [True]
    assert output == "Initialisation de la configuration terminée.\n"
