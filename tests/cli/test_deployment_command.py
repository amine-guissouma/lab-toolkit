from types import SimpleNamespace

import pytest

from lab_toolkit.cli.commands import deployment
from lab_toolkit.exceptions import BranchError, ConfigurationError


def test_validate_calls_pipeline(monkeypatch):
    # prepare
    called = []

    monkeypatch.setattr(
        deployment,
        deployment.validate_pipeline.__name__,
        lambda: called.append(True),
    )
    # execute
    result = deployment.validate(SimpleNamespace())

    # test
    assert result == 0
    assert called == [True]


def test_show_config_calls_pipeline(monkeypatch):
    # prepare
    called = []

    monkeypatch.setattr(
        deployment,
        deployment.show_config_pipeline.__name__,
        lambda: called.append(True),
    )
    # execute
    result = deployment.show_config(SimpleNamespace())

    # test
    assert result == 0
    assert called == [True]


def test_apply_config_calls_pipeline(monkeypatch):
    # prepare
    called = []

    monkeypatch.setattr(
        deployment,
        deployment.apply_config_pipeline.__name__,
        lambda: called.append(True),
    )

    # execute
    result = deployment.apply_config(SimpleNamespace())

    # test
    assert result == 0
    assert called == [True]


@pytest.mark.parametrize(
    ("command", "pipeline_name", "exception"),
    [
        ("show_config", "show_config_pipeline", BranchError),
        ("apply_config", "apply_config_pipeline", ConfigurationError),
    ],
)
def test_commands_handle_pipeline_errors(
    monkeypatch,
    command,
    pipeline_name,
    exception,
):

    # prepare
    def raise_error():
        raise exception(["Erreur de test"])

    monkeypatch.setattr(deployment, pipeline_name, raise_error)

    # execute
    result = getattr(deployment, command)(SimpleNamespace())

    # test
    assert result == 1


def test_init_calls_pipeline(monkeypatch):
    """Vérifie que la commande init appelle son pipeline."""

    # prepare
    called = []

    monkeypatch.setattr(
        deployment,
        deployment.init_config_pipeline.__name__,
        lambda: called.append(True),
    )

    # execute
    result = deployment.init(SimpleNamespace())

    # test
    assert result == 0
    assert called == [True]
