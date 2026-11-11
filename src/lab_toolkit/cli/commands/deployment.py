
import subprocess
from pathlib import PurePosixPath

from lab_toolkit.deployment.config import (
    load_config,
    load_expected_config,
)
from lab_toolkit.deployment.git import get_current_branch
from lab_toolkit.deployment.validation import (
    validate_branch,
    validate_config,
    validate_expected_fields,
)


def build_expected_paths(
    branch: str,
    expected_remote_dir: str,
) -> tuple[str, str]:
    """Calcule les chemins attendus selon la branche Git."""

    branch_errors = validate_branch(branch)

    if branch_errors:
        raise ValueError("; ".join(branch_errors))

    root = PurePosixPath(expected_remote_dir)

    if branch == "socle":
        expected_remote = str(root / "socle")
        expected_base = "/"

        return expected_remote, expected_base

    experience_path = branch.removeprefix("experience/")

    expected_remote = str(
        root / "experiences" / experience_path
    )
    expected_base = f"/experiences/{experience_path}/"

    return expected_remote, expected_base


def validate(args):
    """Charge et vérifie les configurations de déploiement."""

    try:
        config = load_config()
        expected_config = load_expected_config()

        expected_errors = validate_expected_fields(expected_config)

        if expected_errors:
            print("Configuration de déploiement attendue invalide :")

            for error in expected_errors:
                print(f"- {error}")

            return 1

        branch = get_current_branch()

    except (
        FileNotFoundError,
        ValueError,
        RuntimeError,
        subprocess.CalledProcessError,
    ) as error:
        print(f"ERREUR : {error}")
        return 1

    try:
        expected_remote, expected_base = build_expected_paths(
            branch,
            expected_config["expectedRemoteDir"],
        )

    except ValueError as error:
        print("Configuration de déploiement invalide :")
        print(f"- {error}")
        return 1

    errors = validate_config(
        config,
        expected_remote,
        expected_base,
    )

    if errors:
        print("Configuration de déploiement invalide :")

        for error in errors:
            print(f"- {error}")

        return 1

    print("Configuration de déploiement valide.")
    return 0


def configure(args):
    print("Configuration du déploiement : fonctionnalité à développer.")


def add_deployment_commands(subparsers):
    deployment_parser = subparsers.add_parser(
        "deployment",
        help="Gestion de la configuration de déploiement.",
    )

    deployment_subparsers = deployment_parser.add_subparsers(
        dest="deployment_command",
        required=True,
    )

    validate_parser = deployment_subparsers.add_parser(
        "validate",
        help="Vérifier la configuration de déploiement.",
    )
    validate_parser.set_defaults(func=validate)

    configure_parser = deployment_subparsers.add_parser(
        "configure",
        help="Préparer la configuration de déploiement.",
    )
    configure_parser.set_defaults(func=configure)
