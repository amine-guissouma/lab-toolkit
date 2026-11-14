from pathlib import Path

from lab_toolkit.deployment.config import load_expected_config
from lab_toolkit.deployment.constants import DEPLOYMENT, DEPLOYMENT_EXPECTED
from lab_toolkit.deployment.git import get_current_branch
from lab_toolkit.deployment.paths import build_expected_paths
from lab_toolkit.deployment.validation import validate_expected_fields


def build_deployment_config(
    project_dir: Path | None = None,
    branch: str | None = None,
) -> dict:
    """Calcule la configuration de déploiement attendue."""

    expected_config = load_expected_config(project_dir)
    validate_expected_fields(expected_config)

    if branch is None:
        branch = get_current_branch()

    expected_remote, expected_base = build_expected_paths(
        branch,
        expected_config[DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR],
    )

    return {
        DEPLOYMENT.REMOTE_DIR: expected_remote,
        DEPLOYMENT.BASE: expected_base,
    }
