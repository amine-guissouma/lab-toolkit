from lab_toolkit.deployment.config import load_config, load_expected_config
from lab_toolkit.deployment.constants import DEPLOYMENT_EXPECTED
from lab_toolkit.deployment.git import get_current_branch
from lab_toolkit.deployment.paths import build_expected_paths
from lab_toolkit.deployment.validation import (
    validate_expected_fields,
    validate_paths,
    validate_required_fields,
)


def validate_pipeline():
    """Orchestre le pipeline complet de validation du déploiement."""

    config = load_config()
    validate_required_fields(config)

    expected_config = load_expected_config()
    validate_expected_fields(expected_config)

    branch = get_current_branch()

    expected_remote, expected_base = build_expected_paths(
        branch,
        expected_config[DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR],
    )

    validate_paths(config, expected_remote, expected_base)

    return {
        "Branche": branch,
        "remoteDir": config.get("remoteDir"),
        "base": config.get("base"),
    }
