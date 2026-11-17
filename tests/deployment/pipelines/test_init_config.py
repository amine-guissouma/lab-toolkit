import json
from unittest.mock import Mock

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
):
    """Vérifie la création des deux fichiers sur socle."""

    # prepare
    monkeypatch.chdir(tmp_path)

    local_branch_mock = Mock(return_value=True)

    monkeypatch.setattr(
        init_config,
        init_config.get_current_branch.__name__,
        lambda: BRANCH.SOCLE,
    )
    monkeypatch.setattr(
        init_config,
        init_config.local_branch_exists.__name__,
        local_branch_mock,
    )

    # execute
    result = init_config.init_config_pipeline()

    # test
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

    assert result == {
        "Branche": BRANCH.SOCLE,
        "deployment.json créé": True,
        "deployment_expected.json créé": True,
    }

    local_branch_mock.assert_called_once_with(BRANCH.SOCLE)


def test_init_config_pipeline_creates_only_missing_expected_file(
    tmp_path,
    monkeypatch,
):
    """Vérifie que seul le fichier expected est créé s'il manque."""

    # prepare
    monkeypatch.chdir(tmp_path)

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
        init_config.get_current_branch.__name__,
        lambda: BRANCH.SOCLE,
    )
    monkeypatch.setattr(
        init_config,
        init_config.local_branch_exists.__name__,
        lambda branch: True,
    )

    # execute
    result = init_config.init_config_pipeline()

    # test
    saved_config = json.loads(deployment_path.read_text(encoding="utf-8"))

    assert saved_config == original_config
    assert (tmp_path / DEPLOYMENT_EXPECTED.FILENAME).is_file()

    assert result == {
        "Branche": BRANCH.SOCLE,
        "deployment.json créé": False,
        "deployment_expected.json créé": True,
    }


def test_init_config_pipeline_creates_only_missing_deployment_file(
    tmp_path,
    monkeypatch,
):
    """Vérifie que seul deployment est créé si le fichier expected existe."""
    # prepare
    monkeypatch.chdir(tmp_path)

    expected_path = tmp_path / DEPLOYMENT_EXPECTED.FILENAME

    original_expected_config = {
        DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR: "/mon-autre-chemin",
    }

    expected_path.write_text(
        json.dumps(original_expected_config),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        init_config,
        init_config.get_current_branch.__name__,
        lambda: BRANCH.SOCLE,
    )
    monkeypatch.setattr(
        init_config,
        init_config.local_branch_exists.__name__,
        lambda branch: True,
    )

    # execute
    result = init_config.init_config_pipeline()

    # test
    saved_expected_config = json.loads(expected_path.read_text(encoding="utf-8"))

    deployment_path = tmp_path / DEPLOYMENT.FILENAME

    assert deployment_path.is_file()
    assert saved_expected_config == original_expected_config

    assert result == {
        "Branche": BRANCH.SOCLE,
        "deployment.json créé": True,
        "deployment_expected.json créé": False,
    }


def test_init_config_pipeline_does_not_modify_existing_files(
    tmp_path,
    monkeypatch,
):
    """Vérifie qu'aucun fichier existant n'est modifié."""

    # prepare
    monkeypatch.chdir(tmp_path)

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
        init_config.get_current_branch.__name__,
        lambda: BRANCH.SOCLE,
    )
    monkeypatch.setattr(
        init_config,
        init_config.local_branch_exists.__name__,
        lambda branch: True,
    )

    # execute
    result = init_config.init_config_pipeline()

    # test
    assert json.loads(deployment_path.read_text(encoding="utf-8")) == deployment_config

    assert json.loads(expected_path.read_text(encoding="utf-8")) == expected_config

    assert result == {
        "Résultat": (
            "Les fichiers de configuration existent déjà. "
            "Aucune modification effectuée."
        ),
    }


def test_init_config_pipeline_requires_socle_branch(
    tmp_path,
    monkeypatch,
):
    """Vérifie que les fichiers ne sont pas créés hors de socle."""

    # prepare
    monkeypatch.chdir(tmp_path)

    local_branch_mock = Mock(return_value=True)

    monkeypatch.setattr(
        init_config,
        init_config.get_current_branch.__name__,
        lambda: "feature/test",
    )
    monkeypatch.setattr(
        init_config,
        init_config.local_branch_exists.__name__,
        local_branch_mock,
    )

    # execute / test
    with pytest.raises(BranchError, match="git switch socle"):
        init_config.init_config_pipeline()

    # test
    local_branch_mock.assert_called_once_with(BRANCH.SOCLE)

    assert not (tmp_path / DEPLOYMENT.FILENAME).exists()
    assert not (tmp_path / DEPLOYMENT_EXPECTED.FILENAME).exists()


def test_init_config_pipeline_requests_socle_creation(
    tmp_path,
    monkeypatch,
):
    """Vérifie les instructions si socle n'existe pas localement."""

    # prepare
    monkeypatch.chdir(tmp_path)

    local_branch_mock = Mock(return_value=False)

    monkeypatch.setattr(
        init_config,
        init_config.get_current_branch.__name__,
        lambda: "feature/test",
    )
    monkeypatch.setattr(
        init_config,
        init_config.local_branch_exists.__name__,
        local_branch_mock,
    )

    # execute / test
    with pytest.raises(BranchError, match="git switch -c socle"):
        init_config.init_config_pipeline()

    # test
    local_branch_mock.assert_called_once_with(BRANCH.SOCLE)

    assert not (tmp_path / DEPLOYMENT.FILENAME).exists()
    assert not (tmp_path / DEPLOYMENT_EXPECTED.FILENAME).exists()
