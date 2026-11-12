
import json
from pathlib import Path

from lab_toolkit.exceptions import ConfigurationError


CONFIG_FILENAME = "deployment.json"
EXPECTED_CONFIG_FILENAME = "deployment_expected.json"


def load_json_file(filename: str, project_dir: Path | None = None) -> dict:
    """Charge un fichier JSON du projet courant."""

    if project_dir is None:
        project_dir = Path.cwd()

    config_path = project_dir / filename

    if not config_path.is_file():
        raise ConfigurationError(
            f"Fichier de configuration introuvable : {config_path}"
        )

    try:
        with config_path.open("r", encoding="utf-8") as config_file:
            config = json.load(config_file)

    except json.JSONDecodeError as error:
        raise ConfigurationError(
            f"Le fichier {filename} contient un JSON invalide : {error}"
        ) from error

    if not isinstance(config, dict):
        raise ConfigurationError(
            f"Le contenu de {filename} doit être un objet JSON."
        )

    return config


def load_config(project_dir: Path | None = None) -> dict:
    """Charge deployment.json."""

    return load_json_file(CONFIG_FILENAME, project_dir)


def load_expected_config(project_dir: Path | None = None) -> dict:
    """Charge deployment_expected.json."""

    return load_json_file(EXPECTED_CONFIG_FILENAME, project_dir)
