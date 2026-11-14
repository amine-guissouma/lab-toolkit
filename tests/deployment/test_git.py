import subprocess

import pytest

from lab_toolkit.deployment.constants import BRANCH
from lab_toolkit.deployment.git import get_current_branch
from lab_toolkit.exceptions import GitError


def test_get_current_branch(monkeypatch):
    """Vérifie la récupération du nom de la branche."""

    stdout = BRANCH.SOCLE

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=0,
            stdout=stdout,
            stderr="",
        )

    monkeypatch.setattr("subprocess.run", mock_run)

    assert get_current_branch() == BRANCH.SOCLE


def test_get_current_branch_empty(monkeypatch):
    """Vérifie le rejet d'un nom de branche vide."""

    stdout = "\n"

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=0,
            stdout=stdout,
            stderr="",
        )

    monkeypatch.setattr("subprocess.run", mock_run)

    with pytest.raises(GitError):
        get_current_branch()
