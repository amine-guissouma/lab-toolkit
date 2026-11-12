from pathlib import PurePosixPath

from lab_toolkit.exceptions import (
    BranchError,
    ConfigurationError,
)

REQUIRED_FIELDS = ("remoteDir", "base")
EXPECTED_REQUIRED_FIELDS = ("expectedRemoteDir",)


def validate_required_fields(config: dict) -> None:
    """Vérifie la présence, le type et la valeur des paramètres."""

    errors = []

    for field in REQUIRED_FIELDS:
        if field not in config:
            errors.append(f"Paramètre manquant : {field}")
            continue

        value = config[field]

        if not isinstance(value, str):
            errors.append(f"Le paramètre {field} doit être une chaîne de caractères.")
        elif not value.strip():
            errors.append(f"Le paramètre {field} ne peut pas être vide.")

    if errors:
        raise ConfigurationError(errors)


def validate_branch(branch: str) -> None:
    """Vérifie que la branche Git est autorisée."""

    errors = []

    if branch == "socle":
        return

    if branch.startswith("experience/"):
        experience_path = branch.removeprefix("experience/")
        path_segments = experience_path.split("/")

        if not experience_path or any(not segment for segment in path_segments):
            errors.append(f"Nom de branche d'expérience invalide : {branch}")

    else:
        errors.append(f"Branche Git non prise en charge : {branch}")

    if errors:
        raise BranchError(errors)


def validate_paths(
    config: dict,
    expected_remote: str,
    expected_base: str,
) -> None:
    """Compare les chemins configurés avec les chemins attendus."""

    errors = []

    if config["remoteDir"] != expected_remote:
        errors.append(
            f"remoteDir incorrect. Attendu : {expected_remote} ; "
            f"obtenu : {config['remoteDir']}"
        )

    if config["base"] != expected_base:
        errors.append(
            f"base incorrecte. Attendu : {expected_base} ; obtenu : {config['base']}"
        )

    if errors:
        raise ConfigurationError(errors)


def validate_expected_fields(config: dict) -> None:
    """Vérifie les paramètres obligatoires de deployment_expected.json."""

    errors = []

    for field in EXPECTED_REQUIRED_FIELDS:
        if field not in config:
            errors.append(f"Paramètre attendu manquant : {field}")
            continue

        value = config[field]

        if not isinstance(value, str):
            errors.append(f"Le paramètre {field} doit être une chaîne de caractères.")
            continue

        if not value.strip():
            errors.append(f"Le paramètre {field} ne peut pas être vide.")
            continue

        if field == "expectedRemoteDir":
            if value != value.strip():
                errors.append(
                    "Le paramètre expectedRemoteDir ne doit pas contenir "
                    "d'espaces au début ou à la fin."
                )

            if not PurePosixPath(value).is_absolute():
                errors.append(
                    "Le paramètre expectedRemoteDir doit être un chemin absolu."
                )

    if errors:
        raise ConfigurationError(errors)
