from pathlib import PurePosixPath

REQUIRED_FIELDS = ("remoteDir", "base")

EXPECTED_REQUIRED_FIELDS = ("expectedRemoteDir",)


def validate_required_fields(config: dict) -> list[str]:
    """Vérifie la présence, le type et la valeur des paramètres."""

    errors = []

    for field in REQUIRED_FIELDS:
        if field not in config:
            errors.append(f"Paramètre manquant : {field}")
            continue

        value = config[field]

        if not isinstance(value, str):
            errors.append(
                f"Le paramètre {field} doit être une chaîne de caractères."
            )
        elif not value.strip():
            errors.append(
                f"Le paramètre {field} ne peut pas être vide."
            )

    return errors


def validate_branch(branch: str) -> list[str]:
    """Vérifie que la branche Git est autorisée."""

    if branch == "socle":
        return []

    if branch.startswith("experience/"):
        experience_path = branch.removeprefix("experience/")
        path_segments = experience_path.split("/")

        if not experience_path or any(
            not segment for segment in path_segments
        ):
            return [
                f"Nom de branche d'expérience invalide : {branch}"
            ]

        return []

    return [
        f"Branche Git non prise en charge : {branch}"
    ]


def validate_paths(
    config: dict,
    expected_remote: str,
    expected_base: str,
) -> list[str]:
    """Compare les chemins configurés avec les chemins attendus."""

    errors = []

    if config["remoteDir"] != expected_remote:
        errors.append(
            f"remoteDir incorrect. Attendu : {expected_remote} ; "
            f"obtenu : {config['remoteDir']}"
        )

    if config["base"] != expected_base:
        errors.append(
            f"base incorrecte. Attendu : {expected_base} ; "
            f"obtenu : {config['base']}"
        )

    return errors


def validate_config(
    config: dict,
    expected_remote: str,
    expected_base: str,
) -> list[str]:
    """Orchestre la validation de la configuration."""

    errors = validate_required_fields(config)

    if errors:
        return errors

    return validate_paths(
        config,
        expected_remote,
        expected_base,
    )

def validate_expected_fields(config: dict) -> list[str]:
    """Vérifie les paramètres obligatoires de deployment_expected.json."""

    errors = []

    for field in EXPECTED_REQUIRED_FIELDS:
        if field not in config:
            errors.append(f"Paramètre attendu manquant : {field}")
            continue

        value = config[field]

        if not isinstance(value, str):
            errors.append(
                f"Le paramètre {field} doit être une chaîne de caractères."
            )
        elif not value.strip():
            errors.append(
                f"Le paramètre {field} ne peut pas être vide."
            )
        elif field == "expectedRemoteDir" and value != value.strip():
            errors.append(
                "Le paramètre expectedRemoteDir ne doit pas contenir "
                "d'espaces au début ou à la fin."
            )
        elif field == "expectedRemoteDir" and not PurePosixPath(value).is_absolute():
            errors.append(
                "Le paramètre expectedRemoteDir doit être un chemin absolu."
            )
    return errors