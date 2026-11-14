from pathlib import PurePosixPath

from lab_toolkit.deployment.constants import BRANCH, DEPLOYMENT
from lab_toolkit.deployment.validation import validate_branch


def build_expected_paths(
    branch: str,
    expected_remote_dir: str,
) -> tuple[str, str]:
    """Calcule les chemins attendus selon la branche Git."""

    validate_branch(branch)

    root = PurePosixPath(expected_remote_dir)

    if branch == BRANCH.SOCLE:
        return get_expected_socle(root)

    return get_expected_experience(branch, root)


def get_expected_socle(
    root: PurePosixPath,
) -> tuple[str, str]:
    """Retourne les chemins attendus pour la branche socle."""

    expected_remote = str(root / BRANCH.SOCLE)
    expected_base = "/"

    return expected_remote, expected_base


def get_expected_experience(
    branch: str,
    root: PurePosixPath,
) -> tuple[str, str]:
    """Retourne les chemins attendus pour une branche expérience."""

    experience_path = branch.removeprefix(BRANCH.EXPERIENCE_PREFIX)

    expected_remote = str(root / DEPLOYMENT.EXPERIENCES_DIR / experience_path)
    expected_base = f"/{DEPLOYMENT.EXPERIENCES_DIR}/{experience_path}/"

    return expected_remote, expected_base
