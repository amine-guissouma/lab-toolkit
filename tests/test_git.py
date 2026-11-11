
import subprocess

import pytest

from lab_toolkit.deployment.git import get_current_branch


def test_get_current_branch(monkeypatch):
    """Vérifie la récupération du nom de la branche."""

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=0,
            stdout="socle\n",
            stderr="",
        )

    monkeypatch.setattr(
        "lab_toolkit.deployment.git.subprocess.run",
        mock_run,
    )

    assert get_current_branch() == "socle"


def test_get_current_branch_empty(monkeypatch):
    """Vérifie le rejet d'un nom de branche vide."""

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=0,
            stdout="\n",
            stderr="",
        )

    monkeypatch.setattr(
        "lab_toolkit.deployment.git.subprocess.run",
        mock_run,
    )

    with pytest.raises(RuntimeError):
        get_current_branch()
