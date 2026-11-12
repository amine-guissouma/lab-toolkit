
from types import SimpleNamespace

from lab_toolkit.cli.commands import deployment
from lab_toolkit.exceptions import BranchError


CURRENT_CONFIG = {
    "remoteDir": "/var/www/labs/test-project",
    "base": "/",
}

PROPOSED_CONFIG = {
    "remoteDir": "/var/www/labs/lab-front-react/socle",
    "base": "/",
}


def test_configure_without_apply_does_not_save(
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

    result = deployment.configure(
        SimpleNamespace(apply=False)
    )

    output = capsys.readouterr().out

    assert result == 0
    assert "Configuration proposée" in output
    assert "Aucune modification effectuée" in output
    assert saved_configs == []


def test_configure_with_apply_saves_config(
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

    result = deployment.configure(
        SimpleNamespace(apply=True)
    )

    output = capsys.readouterr().out

    assert result == 0
    assert saved_configs == [PROPOSED_CONFIG]
    assert "Configuration de déploiement mise à jour." in output


def test_configure_invalid_branch_does_not_save(
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

    result = deployment.configure(
        SimpleNamespace(apply=True)
    )

    output = capsys.readouterr().out

    assert result == 1
    assert "master" in output
    assert saved_configs == []

def test_configure_with_apply_preserves_additional_fields(
    monkeypatch,
    capsys,
):
    current_config = {
        "remoteDir": "/var/www/labs/test-project",
        "base": "/",
        "champ1": "valeur1",
        "champ2": "valeur2",
    }

    proposed_config = {
        "remoteDir": "/var/www/labs/lab-front-react/socle",
        "base": "/",
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
        lambda: proposed_config,
    )
    monkeypatch.setattr(
        deployment,
        "save_config",
        lambda config: saved_configs.append(config),
    )

    result = deployment.configure(
        SimpleNamespace(apply=True)
    )

    capsys.readouterr()

    assert result == 0
    assert saved_configs == [
        {
            "remoteDir": "/var/www/labs/lab-front-react/socle",
            "base": "/",
            "champ1": "valeur1",
            "champ2": "valeur2",
        }
    ]