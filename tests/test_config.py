
import json

import pytest

from lab_toolkit.deployment.config import load_config
from lab_toolkit.deployment.config import load_expected_config

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

    with pytest.raises(FileNotFoundError):
        load_config(tmp_path)


def test_load_config_invalid_json(tmp_path):
    """Vérifie le rejet d'un fichier JSON invalide."""

    config_file = tmp_path / "deployment.json"
    config_file.write_text("{invalid json}", encoding="utf-8")

    with pytest.raises(ValueError):
        load_config(tmp_path)


def test_load_config_requires_json_object(tmp_path):
    """Vérifie que le contenu JSON doit être un objet."""

    config_file = tmp_path / "deployment.json"
    config_file.write_text('["socle", "experience"]', encoding="utf-8")

    with pytest.raises(ValueError):
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

    with pytest.raises(FileNotFoundError):
        load_expected_config(tmp_path)


def test_load_expected_config_invalid_json(tmp_path):
    """Vérifie le rejet d'un JSON invalide."""

    config_file = tmp_path / "deployment_expected.json"
    config_file.write_text("{invalid json}", encoding="utf-8")

    with pytest.raises(ValueError):
        load_expected_config(tmp_path)


def test_load_expected_config_requires_json_object(tmp_path):
    """Vérifie que le contenu doit être un objet JSON."""

    config_file = tmp_path / "deployment_expected.json"
    config_file.write_text('["socle", "experience"]', encoding="utf-8")

    with pytest.raises(ValueError):
        load_expected_config(tmp_path)
