import json
from pathlib import Path

import pytest

from lab_toolkit.deployment.config import load_config, load_expected_config, save_config
from lab_toolkit.exceptions import ConfigurationError


## load_config
def test_load_config_valid(tmp_path):
    """Vérifie le chargement d'une configuration valide."""

    config_data = {
        "remoteDir": "/var/www/labs/lab-front-react/socle",
        "base": "/",
    }

    config_file = tmp_path / "deployment.json"
    config_file.write_text(json.dumps(config_data), encoding="utf-8")

    config = load_config(tmp_path)

    assert config == config_data


def test_load_config_missing_file(tmp_path):
    """Vérifie le comportement si deployment.json est absent."""

    with pytest.raises(ConfigurationError):
        load_config(tmp_path)


def test_load_config_invalid_json(tmp_path):
    """Vérifie le rejet d'un fichier JSON invalide."""

    config_file = tmp_path / "deployment.json"
    config_file.write_text("{invalid json}", encoding="utf-8")

    with pytest.raises(ConfigurationError):
        load_config(tmp_path)


def test_load_config_requires_json_object(tmp_path):
    """Vérifie que le contenu JSON doit être un objet."""

    config_file = tmp_path / "deployment.json"
    config_file.write_text('["socle", "experience"]', encoding="utf-8")

    with pytest.raises(ConfigurationError):
        load_config(tmp_path)


## load_expected_config


def test_load_expected_config_valid(tmp_path):
    """Vérifie le chargement de deployment_expected.json."""

    expected_data = {
        "expectedRemoteDir": "/var/www/labs/lab-front-react",
    }

    config_file = tmp_path / "deployment_expected.json"
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

    config_file = tmp_path / "deployment_expected.json"
    config_file.write_text("{invalid json}", encoding="utf-8")

    with pytest.raises(ConfigurationError):
        load_expected_config(tmp_path)


def test_load_expected_config_requires_json_object(tmp_path):
    """Vérifie que le contenu doit être un objet JSON."""

    config_file = tmp_path / "deployment_expected.json"
    config_file.write_text('["socle", "experience"]', encoding="utf-8")

    with pytest.raises(ConfigurationError):
        load_expected_config(tmp_path)


def test_save_config_valid(tmp_path):
    """Vérifie l'enregistrement d'une configuration."""

    config = {
        "remoteDir": "/var/www/labs/socle",
        "base": "/",
    }

    save_config(config, tmp_path)

    saved_config = json.loads(
        (tmp_path / "deployment.json").read_text(encoding="utf-8")
    )

    assert saved_config == config


def test_save_config_preserves_existing_file_on_write_failure(
    tmp_path,
    monkeypatch,
):
    """Vérifie que l'ancien fichier reste intact si le remplacement échoue."""

    config_file = tmp_path / "deployment.json"
    original_config = {
        "remoteDir": "/var/www/labs/ancien",
        "base": "/",
    }

    config_file.write_text(
        json.dumps(original_config),
        encoding="utf-8",
    )

    def mock_replace(self, target):
        raise OSError("Erreur de remplacement")

    monkeypatch.setattr(type(config_file), "replace", mock_replace)

    new_config = {
        "remoteDir": "/var/www/labs/nouveau",
        "base": "/nouveau/",
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

    content = (tmp_path / "deployment.json").read_text(encoding="utf-8")

    assert "Expérience française" in content


def test_save_config_preserves_existing_file_on_replace_failure(
    tmp_path,
    monkeypatch,
):
    config_path = tmp_path / "deployment.json"
    config_path.write_text(
        '{"remoteDir": "/ancienne-valeur", "base": "/"}',
        encoding="utf-8",
    )

    def fail_replace(self, target):
        raise OSError("Erreur simulée de remplacement")

    monkeypatch.setattr(Path, "replace", fail_replace)

    new_config = {
        "remoteDir": "/nouvelle-valeur",
        "base": "/",
    }

    with pytest.raises(ConfigurationError):
        save_config(new_config, tmp_path)

    assert config_path.read_text(encoding="utf-8") == (
        '{"remoteDir": "/ancienne-valeur", "base": "/"}'
    )

    assert not (tmp_path / "deployment.json.tmp").exists()


def test_save_config_handles_temporary_file_creation_failure(
    tmp_path,
    monkeypatch,
):
    def fail_open(self, *args, **kwargs):
        raise OSError("Erreur simulée de création")

    monkeypatch.setattr(Path, "open", fail_open)

    with pytest.raises(ConfigurationError):
        save_config(
            {"remoteDir": "/nouvelle-valeur", "base": "/"},
            tmp_path,
        )
