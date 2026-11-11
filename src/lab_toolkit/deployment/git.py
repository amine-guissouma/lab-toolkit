
import subprocess
from pathlib import Path

def get_current_branch() -> str:
    """Retourne le nom de la branche Git courante."""

    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=Path.cwd(),
        capture_output=True,
        text=True,
        check=True,
    )

    branch = result.stdout.strip()

    if not branch:
        raise RuntimeError(
            "Impossible de déterminer la branche Git courante."
        )

    return branch