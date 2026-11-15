import json

import pytest

from lab_toolkit.deployment.constants import (
    BRANCH,
    DEPLOYMENT,
    DEPLOYMENT_EXPECTED,
)
from lab_toolkit.deployment.pipeline import init_config
from lab_toolkit.exceptions import BranchError


def test_init_config_pipeline_creates_both_files(
    tmp_path,
    monkeypatch,
    capsys,
):
    """Vérifie la création des deux fichiers sur socle."""

    monkeypatch.setattr(
        init_config,
        "get_current_branch",
        lambda: BRANCH.SOCLE,
    )

    init_config.init_config_pipeline(tmp_path)

    deployment_config = json.loads(
        (tmp_path / DEPLOYMENT.FILENAME).read_text(encoding="utf-8")
    )
    expected_config = json.loads(
        (tmp_path / DEPLOYMENT_EXPECTED.FILENAME).read_text(encoding="utf-8")
    )

    assert deployment_config == {
        DEPLOYMENT.REMOTE_DIR: DEPLOYMENT.DEFAULT_REMOTE_DIR,
        DEPLOYMENT.BASE: DEPLOYMENT.DEFAULT_BASE,
    }

    assert expected_config == {
        DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR: (
            DEPLOYMENT_EXPECTED.DEFAULT_EXPECTED_REMOTE_DIR
        ),
    }

    output = capsys.readouterr().out

    assert f"{DEPLOYMENT.FILENAME} créé." in output
    assert f"{DEPLOYMENT_EXPECTED.FILENAME} créé." in output
    assert "un-configured" in output


def test_init_config_pipeline_creates_only_missing_file(
    tmp_path,
    monkeypatch,
    capsys,
):
    """Vérifie qu'un seul fichier manquant est créé."""

    deployment_path = tmp_path / DEPLOYMENT.FILENAME

    original_config = {
        DEPLOYMENT.REMOTE_DIR: "/mon-chemin",
        DEPLOYMENT.BASE: "/",
    }

    deployment_path.write_text(
        json.dumps(original_config),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        init_config,
        "get_current_branch",
        lambda: BRANCH.SOCLE,
    )

    init_config.init_config_pipeline(tmp_path)

    saved_config = json.loads(deployment_path.read_text(encoding="utf-8"))

    assert saved_config == original_config
    assert (tmp_path / DEPLOYMENT_EXPECTED.FILENAME).is_file()

    output = capsys.readouterr().out

    assert f"{DEPLOYMENT_EXPECTED.FILENAME} créé." in output
    assert f"{DEPLOYMENT.FILENAME} créé." not in output


def test_init_config_pipeline_does_not_modify_existing_files(
    tmp_path,
    monkeypatch,
    capsys,
):
    """Vérifie qu'aucun fichier existant n'est modifié."""

    deployment_config = {
        DEPLOYMENT.REMOTE_DIR: "/mon-chemin",
        DEPLOYMENT.BASE: "/",
    }

    expected_config = {
        DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR: "/mon-autre-chemin",
    }

    deployment_path = tmp_path / DEPLOYMENT.FILENAME
    expected_path = tmp_path / DEPLOYMENT_EXPECTED.FILENAME

    deployment_path.write_text(
        json.dumps(deployment_config),
        encoding="utf-8",
    )
    expected_path.write_text(
        json.dumps(expected_config),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        init_config,
        "get_current_branch",
        lambda: BRANCH.SOCLE,
    )

    init_config.init_config_pipeline(tmp_path)

    assert json.loads(deployment_path.read_text(encoding="utf-8")) == (
        deployment_config
    )
    assert json.loads(expected_path.read_text(encoding="utf-8")) == (expected_config)

    output = capsys.readouterr().out

    assert "Les fichiers de configuration existent déjà." in output
    assert "Aucune modification effectuée." in output


def test_init_config_pipeline_requires_socle_branch(
    tmp_path,
    monkeypatch,
):
    """Vérifie que les fichiers ne sont pas créés hors de socle."""

    monkeypatch.setattr(
        init_config,
        "get_current_branch",
        lambda: "feature/test",
    )
    monkeypatch.setattr(
        init_config,
        "local_branch_exists",
        lambda branch: True,
    )

    with pytest.raises(BranchError, match="git switch socle"):
        init_config.init_config_pipeline(tmp_path)

    assert not (tmp_path / DEPLOYMENT.FILENAME).exists()
    assert not (tmp_path / DEPLOYMENT_EXPECTED.FILENAME).exists()


def test_init_config_pipeline_requests_socle_creation(
    tmp_path,
    monkeypatch,
):
    """Vérifie les instructions si socle n'existe pas localement."""

    monkeypatch.setattr(
        init_config,
        "get_current_branch",
        lambda: "feature/test",
    )
    monkeypatch.setattr(
        init_config,
        "local_branch_exists",
        lambda branch: False,
    )

    with pytest.raises(BranchError, match="git switch -c socle"):
        init_config.init_config_pipeline(tmp_path)

    assert not (tmp_path / DEPLOYMENT.FILENAME).exists()
    assert not (tmp_path / DEPLOYMENT_EXPECTED.FILENAME).exists()
