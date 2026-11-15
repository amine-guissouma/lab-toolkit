import json
from pathlib import Path

import pytest

from lab_toolkit.deployment.config import load_config, load_expected_config, save_config
from lab_toolkit.deployment.constants import BRANCH, DEPLOYMENT, DEPLOYMENT_EXPECTED
from lab_toolkit.exceptions import ConfigurationError

EXPECTED_REMOTE_DIR = "/var/www/labs/lab-front-react"


def test_load_config_valid(tmp_path):
    """Vérifie le chargement d'une configuration valide."""

    config_data = {
        DEPLOYMENT.REMOTE_DIR: f"{EXPECTED_REMOTE_DIR}/{BRANCH.SOCLE}",
        DEPLOYMENT.BASE: "/",
    }

    config_file = tmp_path / DEPLOYMENT.FILENAME
    config_file.write_text(json.dumps(config_data), encoding="utf-8")

    config = load_config(tmp_path)

    assert config == config_data


def test_load_config_missing_file(tmp_path):
    """Vérifie le comportement si deployment.json est absent."""

    with pytest.raises(ConfigurationError):
        load_config(tmp_path)


def test_load_config_invalid_json(tmp_path):
    """Vérifie le rejet d'un fichier JSON invalide."""

    config_file = tmp_path / DEPLOYMENT.FILENAME
    config_file.write_text("{invalid json}", encoding="utf-8")

    with pytest.raises(ConfigurationError):
        load_config(tmp_path)


def test_load_config_requires_json_object(tmp_path):
    """Vérifie que le contenu JSON doit être un objet."""

    config_file = tmp_path / DEPLOYMENT.FILENAME
    config_file.write_text(
        f"[{BRANCH.SOCLE}, {BRANCH.EXPERIENCE_PREFIX}]", encoding="utf-8"
    )

    with pytest.raises(ConfigurationError):
        load_config(tmp_path)


## load_expected_config


def test_load_expected_config_valid(tmp_path):
    """Vérifie le chargement de deployment_expected.json."""

    expected_data = {
        DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR: EXPECTED_REMOTE_DIR,
    }

    config_file = tmp_path / DEPLOYMENT_EXPECTED.FILENAME
    config_file.write_text(
        json.dumps(expected_data),
        encoding="utf-8",
    )

    config = load_expected_config(tmp_path)

    assert config == expected_data


def test_load_expected_config_missing_file(tmp_path):
    """Vérifie le comportement si le fichier est absent."""

    with pytest.raises(ConfigurationError):
        load_expected_config(tmp_path)


def test_load_expected_config_invalid_json(tmp_path):
    """Vérifie le rejet d'un JSON invalide."""

    config_file = tmp_path / DEPLOYMENT_EXPECTED.FILENAME
    config_file.write_text("{invalid json}", encoding="utf-8")

    with pytest.raises(ConfigurationError):
        load_expected_config(tmp_path)


def test_load_expected_config_requires_json_object(tmp_path):
    """Vérifie que le contenu doit être un objet JSON."""

    config_file = tmp_path / DEPLOYMENT_EXPECTED.FILENAME
    config_file.write_text(
        f"[{BRANCH.SOCLE}, {BRANCH.EXPERIENCE_PREFIX}]", encoding="utf-8"
    )

    with pytest.raises(ConfigurationError):
        load_expected_config(tmp_path)


def test_save_config_valid(tmp_path):
    """Vérifie l'enregistrement d'une configuration."""

    config = {
        DEPLOYMENT.REMOTE_DIR: "/var/www/labs/socle",
        DEPLOYMENT.BASE: "/",
    }

    save_config(config, tmp_path)

    saved_config = json.loads(
        (tmp_path / DEPLOYMENT.FILENAME).read_text(encoding="utf-8")
    )

    assert saved_config == config


def test_save_config_preserves_existing_file_on_write_failure(
    tmp_path,
    monkeypatch,
):
    """Vérifie que l'ancien fichier reste intact si le remplacement échoue."""

    config_file = tmp_path / DEPLOYMENT.FILENAME
    original_config = {
        DEPLOYMENT.REMOTE_DIR: "/var/www/labs/ancien",
        DEPLOYMENT.BASE: "/",
    }

    config_file.write_text(
        json.dumps(original_config),
        encoding="utf-8",
    )

    def mock_replace(self, target):
        raise OSError("Erreur de remplacement")

    monkeypatch.setattr(type(config_file), "replace", mock_replace)

    new_config = {
        DEPLOYMENT.REMOTE_DIR: "/var/www/labs/nouveau",
        DEPLOYMENT.BASE: "/nouveau/",
    }

    with pytest.raises(ConfigurationError):
        save_config(new_config, tmp_path)

    saved_config = json.loads(config_file.read_text(encoding="utf-8"))

    assert saved_config == original_config


def test_save_config_supports_unicode(tmp_path):
    """Vérifie l'enregistrement des caractères Unicode."""

    config = {
        "description": "Expérience française",
    }

    save_config(config, tmp_path)

    content = (tmp_path / DEPLOYMENT.FILENAME).read_text(encoding="utf-8")

    assert "Expérience française" in content


def test_save_config_preserves_existing_file_on_replace_failure(
    tmp_path,
    monkeypatch,
):
    # prepare
    config_path = tmp_path / DEPLOYMENT.FILENAME

    remote_dir_value_old = "/ancienne-valeur"

    original_config = {
        DEPLOYMENT.REMOTE_DIR: remote_dir_value_old,
        DEPLOYMENT.BASE: "/",
    }

    config_path.write_text(
        json.dumps(original_config),
        encoding="utf-8",
    )

    def fail_replace(self, target):
        raise OSError("Erreur simulée de remplacement")

    monkeypatch.setattr(Path, "replace", fail_replace)

    new_config = {
        DEPLOYMENT.REMOTE_DIR: "/nouvelle-valeur",
        DEPLOYMENT.BASE: "/",
    }

    # test raises ConfigurationError
    with pytest.raises(ConfigurationError):
        save_config(new_config, tmp_path)

    # test
    assert json.loads(config_path.read_text(encoding="utf-8")) == original_config
    assert not (tmp_path / "deployment.json.tmp").exists()


def test_save_config_handles_temporary_file_creation_failure(
    tmp_path,
    monkeypatch,
):
    # prepare
    def fail_open(self, *args, **kwargs):
        raise OSError("Erreur simulée de création")

    monkeypatch.setattr(Path, "open", fail_open)

    # test raises ConfigurationError
    with pytest.raises(ConfigurationError):
        # execute
        save_config(
            {DEPLOYMENT.REMOTE_DIR: "/nouvelle-valeur", DEPLOYMENT.BASE: "/"},
            tmp_path,
        )


def test_load_config_supports_utf8_bom(tmp_path):
    # prepare
    config_path = tmp_path / DEPLOYMENT.FILENAME

    remote_dir_value = "/var/www/test"
    base_value = "/"

    config_data = {
        DEPLOYMENT.REMOTE_DIR: remote_dir_value,
        DEPLOYMENT.BASE: base_value,
    }
    config_path.write_text(
        "\ufeff" + json.dumps(config_data),
        encoding="utf-8",
    )

    # execute
    config = load_config(tmp_path)

    # test
    assert config == {
        DEPLOYMENT.REMOTE_DIR: remote_dir_value,
        DEPLOYMENT.BASE: base_value,
    }


def test_create_json_file_if_missing(tmp_path):
    """Vérifie la création d'un fichier JSON absent."""

    from lab_toolkit.deployment.config import create_json_file_if_missing

    config = {
        DEPLOYMENT.REMOTE_DIR: DEPLOYMENT.DEFAULT_REMOTE_DIR,
        DEPLOYMENT.BASE: DEPLOYMENT.DEFAULT_BASE,
    }

    created = create_json_file_if_missing(
        DEPLOYMENT.FILENAME,
        config,
        tmp_path,
    )

    saved_config = json.loads(
        (tmp_path / DEPLOYMENT.FILENAME).read_text(encoding="utf-8")
    )

    assert created is True
    assert saved_config == config


def test_create_json_file_if_missing_does_not_overwrite(tmp_path):
    """Vérifie qu'un fichier existant n'est jamais écrasé."""

    from lab_toolkit.deployment.config import create_json_file_if_missing

    config_path = tmp_path / DEPLOYMENT.FILENAME
    original_config = {
        DEPLOYMENT.REMOTE_DIR: "/ancienne-valeur",
        DEPLOYMENT.BASE: "/",
    }

    config_path.write_text(
        json.dumps(original_config),
        encoding="utf-8",
    )

    created = create_json_file_if_missing(
        DEPLOYMENT.FILENAME,
        {
            DEPLOYMENT.REMOTE_DIR: DEPLOYMENT.DEFAULT_REMOTE_DIR,
            DEPLOYMENT.BASE: DEPLOYMENT.DEFAULT_BASE,
        },
        tmp_path,
    )

    saved_config = json.loads(config_path.read_text(encoding="utf-8"))

    assert created is False
    assert saved_config == original_config
