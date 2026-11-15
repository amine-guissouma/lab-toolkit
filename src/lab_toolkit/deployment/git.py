import subprocess
from pathlib import Path

from lab_toolkit.exceptions import GitError


def get_current_branch() -> str:
    """Retourne le nom de la branche Git courante."""

    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=Path.cwd(),
            capture_output=True,
            text=True,
            check=True,
        )

    except subprocess.CalledProcessError as error:
        raise GitError("Impossible de récupérer la branche Git courante.") from error

    branch = result.stdout.strip()

    if not branch:
        raise GitError("Impossible de déterminer la branche Git courante.")

    return branch


def local_branch_exists(branch: str) -> bool:
    """Vérifie si une branche Git existe localement."""

    try:
        result = subprocess.run(
            ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
            cwd=Path.cwd(),
            capture_output=True,
            text=True,
            check=False,
        )

    except OSError as error:
        raise GitError(
            "Impossible de vérifier l'existence de la branche Git."
        ) from error

    if result.returncode == 0:
        return True

    if result.returncode == 1:
        return False

    raise GitError(f"Impossible de vérifier l'existence de la branche locale {branch}.")
