from pathlib import Path

from lab_toolkit.deployment.config import create_json_file_if_missing
from lab_toolkit.deployment.constants import (
    BRANCH,
    DEPLOYMENT,
    DEPLOYMENT_EXPECTED,
)
from lab_toolkit.deployment.git import (
    get_current_branch,
    local_branch_exists,
)
from lab_toolkit.exceptions import BranchError


def init_config_pipeline(project_dir: Path | None = None) -> None:
    """Initialise les fichiers de configuration sur la branche socle."""

    current_branch = get_current_branch()

    if current_branch != BRANCH.SOCLE:
        if local_branch_exists(BRANCH.SOCLE):
            raise BranchError(
                [
                    f"La commande doit être exécutée sur la branche locale "
                    f"{BRANCH.SOCLE}.",
                    "Veuillez changer de branche avec la commande :",
                    f"git switch {BRANCH.SOCLE}",
                    "Puis relancez :",
                    "lab-toolkit deployment init",
                ]
            )

        raise BranchError(
            [
                f"La branche locale {BRANCH.SOCLE} n'existe pas.",
                "Veuillez la créer et basculer dessus avec les commandes :",
                f"git switch -c {BRANCH.SOCLE}",
                "Puis relancez :",
                "lab-toolkit deployment init",
            ]
        )

    deployment_config = {
        DEPLOYMENT.REMOTE_DIR: DEPLOYMENT.DEFAULT_REMOTE_DIR,
        DEPLOYMENT.BASE: DEPLOYMENT.DEFAULT_BASE,
    }

    expected_config = {
        DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR: (
            DEPLOYMENT_EXPECTED.DEFAULT_EXPECTED_REMOTE_DIR
        ),
    }

    deployment_created = create_json_file_if_missing(
        DEPLOYMENT.FILENAME,
        deployment_config,
        project_dir,
    )

    expected_created = create_json_file_if_missing(
        DEPLOYMENT_EXPECTED.FILENAME,
        expected_config,
        project_dir,
    )

    if deployment_created:
        print(f"Fichier {DEPLOYMENT.FILENAME} créé.")

    if expected_created:
        print(f"Fichier {DEPLOYMENT_EXPECTED.FILENAME} créé.")
        print(
            f"ATTENTION : remplacez 'un-configured' par le chemin réel "
            f"dans {DEPLOYMENT_EXPECTED.FILENAME}."
        )

    if not deployment_created and not expected_created:
        print("Les fichiers de configuration existent déjà.")
        print("Aucune modification effectuée.")
