from pathlib import PurePosixPath

from lab_toolkit.deployment.constants import BRANCH, DEPLOYMENT, DEPLOYMENT_EXPECTED
from lab_toolkit.exceptions import (
    BranchError,
    ConfigurationError,
)

REQUIRED_FIELDS = (DEPLOYMENT.REMOTE_DIR, DEPLOYMENT.BASE)
EXPECTED_REQUIRED_FIELDS = (DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR,)


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

    if branch == BRANCH.SOCLE:
        return

    if branch.startswith(BRANCH.EXPERIENCE_PREFIX):
        experience_path = branch.removeprefix(BRANCH.EXPERIENCE_PREFIX)
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

    if config[DEPLOYMENT.REMOTE_DIR] != expected_remote:
        errors.append(
            f"{DEPLOYMENT.REMOTE_DIR} incorrect. Attendu : {expected_remote} ; "
            f"obtenu : {config[DEPLOYMENT.REMOTE_DIR]}"
        )

    if config[DEPLOYMENT.BASE] != expected_base:
        errors.append(
            f"{DEPLOYMENT.BASE} incorrecte. Attendu : {expected_base} ; "
            f"obtenu : {config[DEPLOYMENT.BASE]}"
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

        if field == DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR:
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


def validate_socle_current_branche(current_branch: str, is_socle_exists: bool):
    if not is_socle_exists:
        raise BranchError(
            [
                f"ATTENTION La branche locale {BRANCH.SOCLE} n'existe pas.",
                "Veuillez la créer et basculer dessus avec les commandes :",
                f"git switch -c {BRANCH.SOCLE}",
                "Puis relancez :",
                "lab-toolkit deployment init",
            ]
        )
    if current_branch != BRANCH.SOCLE:
        raise BranchError(
            [
                f"ATTENTION La commande doit être exécutée sur la branche locale {BRANCH.SOCLE}.",
                "Veuillez changer de branche avec la commande :",
                f"git switch {BRANCH.SOCLE}",
                "Puis relancez :",
                "lab-toolkit deployment init",
            ]
        )
