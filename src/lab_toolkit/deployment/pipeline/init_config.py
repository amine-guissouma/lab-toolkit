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
from lab_toolkit.deployment.validation import validate_socle_current_branche


def init_config_pipeline():
    """Initialise les fichiers de configuration sur la branche socle."""

    current_branch = get_current_branch()
    is_socle_exists = local_branch_exists(BRANCH.SOCLE)

    validate_socle_current_branche(current_branch, is_socle_exists)

    deployment_config = {
        DEPLOYMENT.REMOTE_DIR: DEPLOYMENT.DEFAULT_REMOTE_DIR,
        DEPLOYMENT.BASE: DEPLOYMENT.DEFAULT_BASE,
    }
    deployment_created = create_json_file_if_missing(
        DEPLOYMENT.FILENAME,
        deployment_config,
    )

    expected_config = {
        DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR: DEPLOYMENT_EXPECTED.DEFAULT_EXPECTED_REMOTE_DIR,
    }
    expected_created = create_json_file_if_missing(
        DEPLOYMENT_EXPECTED.FILENAME,
        expected_config,
    )

    if not deployment_created and not expected_created:
        return {
            "Résultat": "Les fichiers de configuration existent déjà. Aucune modification effectuée.",
        }

    return {
        "Branche": current_branch,
        "deployment.json créé": deployment_created,
        "deployment_expected.json créé": expected_created,
    }
