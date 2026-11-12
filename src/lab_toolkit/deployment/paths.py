
from pathlib import PurePosixPath

from lab_toolkit.deployment.validation import validate_branch


def build_expected_paths(
    branch: str,
    expected_remote_dir: str,
) -> tuple[str, str]:
    """Calcule les chemins attendus selon la branche Git."""

    validate_branch(branch)

    root = PurePosixPath(expected_remote_dir)

    if branch == "socle":
        return get_expected_socle(root)

    return get_expected_experience(branch, root)


def get_expected_socle(
    root: PurePosixPath,
) -> tuple[str, str]:
    """Retourne les chemins attendus pour la branche socle."""

    expected_remote = str(root / "socle")
    expected_base = "/"

    return expected_remote, expected_base


def get_expected_experience(
    branch: str,
    root: PurePosixPath,
) -> tuple[str, str]:
    """Retourne les chemins attendus pour une branche expérience."""

    experience_path = branch.removeprefix("experience/")

    expected_remote = str(
        root / "experiences" / experience_path
    )
    expected_base = f"/experiences/{experience_path}/"

    return expected_remote, expected_base
