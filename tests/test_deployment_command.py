from types import SimpleNamespace

from lab_toolkit.cli.commands import deployment
from lab_toolkit.exceptions import BranchError, ConfigurationError

CURRENT_CONFIG = {
    "remoteDir": "/var/www/labs/test-project",
    "base": "/",
}

PROPOSED_CONFIG = {
    "remoteDir": "/var/www/labs/lab-front-react/socle",
    "base": "/",
}


def test_show_config_displays_configuration_without_saving(
    monkeypatch,
    capsys,
):
    saved_configs = []

    monkeypatch.setattr(
        deployment,
        "load_config",
        lambda: CURRENT_CONFIG,
    )
    monkeypatch.setattr(
        deployment,
        "build_deployment_config",
        lambda: PROPOSED_CONFIG,
    )
    monkeypatch.setattr(
        deployment,
        "save_config",
        lambda config: saved_configs.append(config),
    )

    result = deployment.show_config(SimpleNamespace())

    output = capsys.readouterr().out

    assert result == 0
    assert "Configuration actuelle" in output
    assert "Configuration proposée" in output
    assert "Aucune modification effectuée" in output
    assert saved_configs == []


def test_show_config_handles_invalid_branch(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        deployment,
        "load_config",
        lambda: CURRENT_CONFIG,
    )

    def raise_branch_error():
        raise BranchError(["Branche Git non prise en charge : master"])

    monkeypatch.setattr(
        deployment,
        "build_deployment_config",
        raise_branch_error,
    )

    result = deployment.show_config(SimpleNamespace())

    output = capsys.readouterr().out

    assert result == 1
    assert "master" in output


def test_apply_config_saves_configuration(
    monkeypatch,
    capsys,
):
    saved_configs = []

    monkeypatch.setattr(
        deployment,
        "load_config",
        lambda: CURRENT_CONFIG,
    )
    monkeypatch.setattr(
        deployment,
        "build_deployment_config",
        lambda: PROPOSED_CONFIG,
    )
    monkeypatch.setattr(
        deployment,
        "save_config",
        lambda config: saved_configs.append(config),
    )

    result = deployment.apply_config(SimpleNamespace())

    output = capsys.readouterr().out

    assert result == 0
    assert saved_configs == [PROPOSED_CONFIG]
    assert "Configuration de déploiement mise à jour." in output


def test_apply_config_preserves_additional_fields(
    monkeypatch,
):
    current_config = {
        **CURRENT_CONFIG,
        "champ1": "valeur1",
        "champ2": "valeur2",
    }

    saved_configs = []

    monkeypatch.setattr(
        deployment,
        "load_config",
        lambda: current_config,
    )
    monkeypatch.setattr(
        deployment,
        "build_deployment_config",
        lambda: PROPOSED_CONFIG,
    )
    monkeypatch.setattr(
        deployment,
        "save_config",
        lambda config: saved_configs.append(config),
    )

    result = deployment.apply_config(SimpleNamespace())

    assert result == 0
    assert saved_configs == [
        {
            **PROPOSED_CONFIG,
            "champ1": "valeur1",
            "champ2": "valeur2",
        }
    ]


def test_apply_config_handles_invalid_branch(
    monkeypatch,
    capsys,
):
    saved_configs = []

    monkeypatch.setattr(
        deployment,
        "load_config",
        lambda: CURRENT_CONFIG,
    )

    def raise_branch_error():
        raise BranchError(["Branche Git non prise en charge : master"])

    monkeypatch.setattr(
        deployment,
        "build_deployment_config",
        raise_branch_error,
    )
    monkeypatch.setattr(
        deployment,
        "save_config",
        lambda config: saved_configs.append(config),
    )

    result = deployment.apply_config(SimpleNamespace())

    output = capsys.readouterr().out

    assert result == 1
    assert "master" in output
    assert saved_configs == []


def test_show_config_handles_configuration_error(
    monkeypatch,
    capsys,
):
    def raise_configuration_error():
        raise ConfigurationError(["Fichier de configuration introuvable."])

    monkeypatch.setattr(
        deployment,
        "load_config",
        raise_configuration_error,
    )

    result = deployment.show_config(SimpleNamespace())

    output = capsys.readouterr().out

    assert result == 1
    assert "Fichier de configuration introuvable" in output


def test_apply_config_handles_save_error(
    monkeypatch,
    capsys,
):
    def raise_save_error(config):
        raise ConfigurationError(["Impossible d'enregistrer deployment.json."])

    monkeypatch.setattr(
        deployment,
        "load_config",
        lambda: CURRENT_CONFIG,
    )
    monkeypatch.setattr(
        deployment,
        "build_deployment_config",
        lambda: PROPOSED_CONFIG,
    )
    monkeypatch.setattr(
        deployment,
        "save_config",
        raise_save_error,
    )

    result = deployment.apply_config(SimpleNamespace())

    output = capsys.readouterr().out

    assert result == 1
    assert "Impossible d'enregistrer" in output
